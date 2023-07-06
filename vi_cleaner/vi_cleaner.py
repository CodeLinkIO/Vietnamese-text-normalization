import re
import unicodedata
from underthesea import word_tokenize, sent_tokenize

import numpy as np
import torch
from torch.nn.functional import softmax
from transformers import AutoModelForMaskedLM, AutoTokenizer
from .passage_utils import combine_passages, split_long_passages, split_text_passages

from .sentence_utils import get_pieces


from .letter_vi import normalize_letter_vi
from .currency_vi import normalize_currency_vi
from .acronym_vi import spell_acronyms_vi
from .numberical_vi import normalize_number_vi
from .measurement_vi import normalize_measurement_vi
from .datestime_vi import normalize_date, normalize_time
from .roman_number_vi import normalize_roman_numbers
from .abbreviation_vi import normalize_abbreviations_vi
from .symbol_vi import DEFAULT_PIECE_MAX_LENGTH, DEFAULT_SENTENCE_MAX_LENGTH, opening_brackets_and_punctutations_re, punctutations_re
from typing import List


class MLMScorer():
    def __init__(self, model_name: str='', device: str = ''):
        pass
    def score_sentences(self, sentences: List[str]):
        """
        returns list of MLM scores for each sentence in list.
        """
        return [0.0 for _ in sentences]

    def score_sentence(self, sentence: str):
        """
        returns MLM score for sentence.
        """
        return 0.0



class RealMLMScorer(MLMScorer):
    def __init__(self, model_name: str, device: str = 'cpu'):
        """
        Creates MLM scorer from https://arxiv.org/abs/1910.14659.
        Args:
            model_name: HuggingFace pretrained model name
            device: either 'cpu' or 'cuda'
        """
        self.model = AutoModelForMaskedLM.from_pretrained(model_name).to(device).eval()
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        self.device = device
        self.MASK_LABEL = self.tokenizer.mask_token

    def score_sentences(self, sentences: List[str]):
        """
        returns list of MLM scores for each sentence in list.
        """
        return [self.score_sentence(sentence) for sentence in sentences]

    def score_sentence(self, sentence: str):
        """
        returns MLM score for sentence.
        """
        assert type(sentence) == str

        tokens = self.tokenizer.tokenize(sentence)
        mask_idx = []
        token_type = []
        attn_mask = []
        ids = []
        for m_idx, _ in enumerate(tokens):
            masked = self.__mask_text__(m_idx, tokens)
            mask_idx.append(m_idx)
           # ids.append(self.tokenizer.encode(masked))
            ids.append(self.tokenizer.convert_tokens_to_ids([self.tokenizer.cls_token] + masked + [self.tokenizer.sep_token]))
            id_len = len(ids[-1])
            token_type.append([0] * id_len)
            attn_mask.append([1] * id_len)

        data = {
            'input_ids': torch.tensor(ids, device=self.device),
            'attention_mask': torch.tensor(attn_mask, device=self.device),
            'token_type_ids': torch.tensor(token_type, device=self.device),
        }

        with torch.no_grad():
            outputs = self.model(**data)
            logits = outputs.logits
       
        
        scores = []
        scores_log_prob = 0.0

        for i, m_idx in enumerate(mask_idx):
            preds = logits[i].squeeze(0)
            probs = softmax(preds, dim=1)

            token_id = self.tokenizer.convert_tokens_to_ids([tokens[m_idx]])[0]
            log_prob = np.log(probs[m_idx + 1, token_id].cpu().numpy()).item()
           
            scores.append(log_prob)
            scores_log_prob += log_prob

        return scores_log_prob

    def __mask_text__(self, idx: int, tokens: List[str]):
        """
        replaces string at index idx in list `tokens` with a masked token and returns the modified list. 
        """
        masked = tokens.copy()
        masked[idx] = self.MASK_LABEL
        return masked


class ViCleaner(object):
    def __init__(self, text="", model_name ='vinai/phobert-base', ignore_ambiguity=True):
        text = self.collapse_whitespace(text)
        self.text = " " + text + " "
        self.ignore_ambiguity = ignore_ambiguity
        self.scorer = MLMScorer() if ignore_ambiguity else RealMLMScorer(model_name=model_name, device='cuda' if torch.cuda.is_available() else 'cpu')
        
    def join_lines(self, text):
        return text.replace("\n", " ")

    def _collapse_whitespace_before_punctuation(self, match):
        space, punctuation = match.groups(0)
        return punctuation

    def _collapse_whitespace_after_bracket(self, match):
        punctuation, space = match.groups(0)
        return space + punctuation

    def collapse_whitespace(self, text):
        text = re.sub(r"(\s)\1{1,}", r"\1", text)
        text = re.sub(punctutations_re,
                      self._collapse_whitespace_before_punctuation, text)
        text = re.sub(opening_brackets_and_punctutations_re,
                      self._collapse_whitespace_after_bracket, text)
        text = re.sub(r"(\s)\1{1,}", r"\1", text)
        text = re.sub(r"\t+", " ", text)
        text = text.strip()
        return text

    def lowercase(self, text):
        return text.lower()

    def clean_basic(self, text):
        text = self.collapse_whitespace(text)
        text = " " + text + " "
        return text

    def normalize_ascii_vi(self, text):
        return unicodedata.normalize("NFC", text)

    def expand_abbreviations(self, text):
        text = normalize_abbreviations_vi(text)
        return text

    def expand_acronyms(self, text):
        return spell_acronyms_vi(text)

    def expand_roman_numbers(self, text):
        return normalize_roman_numbers(text)

    def expand_date_time(self, text):
        text = normalize_date(text, ignore_ambiguity=self.ignore_ambiguity)
        text = normalize_time(text)
        return text
    
    def expand_versioning(self, text):
        regex = r'\b\d(\.\d{1,2})+\b'
        def repl(m):
            text = m.group(0)
            return ' chấm '.join(text.split('.'))
        text = re.sub(regex, repl, text)
        return text
        

    def change_bon_to_tu(self, text):
        text = re.sub("tháng bốn", "tháng tư", text, flags=re.IGNORECASE)
        text=  re.sub("phần bốn", "phần tư", text, flags=re.IGNORECASE)
        return text
    

    def expand_measurement_units(self, text):
        return normalize_measurement_vi(text)

    def expand_currency(self, text):
        return normalize_currency_vi(text)

    def expand_number(self, text):
        return normalize_number_vi(text)

    def expand_letter(self, text):
        return normalize_letter_vi(text)

    def remove_left_hyphen(self, text):
        return re.sub(r"([^\s])(-)([^\s])", r"\1 \3", text)

    def normalize_linebreak(self, text):
        return [e.strip() for e in re.split(r'[\n]+', text)]
    
    def get_dsd_candicates(self, dsd:str):
        candidate_replacements = []
        head, tail = dsd.split('/')
        head = f' {head}'
        tail = f' {tail}'

        # calculations
        c = f'{self.expand_number(head)} chia {self.expand_number(tail)}'
        c = self.collapse_whitespace(c)
        candidate_replacements.append(c)

        # ratio
        c = f'{self.expand_number(head)} phần {self.expand_number(tail)}'
        c = self.collapse_whitespace(c)
        c = self.change_bon_to_tu(c)
        candidate_replacements.append(c)

        # 'out of'
        c = f'{self.expand_number(head)} trong số {self.expand_number(tail)}'
        c = self.collapse_whitespace(c)
        candidate_replacements.append(c)

        # symbol
        c = f'{self.expand_number(head)} xẹt {self.expand_number(tail)}'
        c = self.collapse_whitespace(c)
        candidate_replacements.append(c)

        # datetime
        # dd/mm candidate
        if float(tail) <= 12 and float(head) <= 31:
            c = f'ngày {self.expand_number(head)} tháng {self.expand_number(tail)}'
            c = self.collapse_whitespace(c)
            c = self.change_bon_to_tu(c)
            candidate_replacements.append(c)

        # mm/yy candidate
        if float(head) <= 12:
            c = f'tháng {self.expand_number(head)} năm {self.expand_number(tail)}'
            c = self.collapse_whitespace(c)
            c = self.change_bon_to_tu(c)
            candidate_replacements.append(c)

        return candidate_replacements
    
    def produce_candidates(self, text):
        dsd_re = r'[\d]+\/[\d]+'
        candidates = [text]

        # dsd - eg. 2/3
        matches = re.findall(dsd_re, text)
        for match in matches:
            candidate_replacements = self.get_dsd_candicates(match)
            candidates = [i.replace(match, j) for i in candidates for j in candidate_replacements]
        # more ambiguity handling to come

        return candidates
   
    def pick_best_candidate(self, candidates):
        if len(candidates) > 1:
            scores = self.scorer.score_sentences(candidates)
            return candidates[scores.index(max(scores))]
        else:
            return candidates[0]
        
    def clean_with_ambiguity(self, text):
        sentences = sent_tokenize(text)
        result = ''
        for sent in sentences:
            candidates = self.produce_candidates(sent)
            best = self.pick_best_candidate(candidates)
            result += best + ' '
        return result

    def clean_text_pre_candidates(self, text:str):
        text = self.collapse_whitespace(text)
        text = " " + text + " "
        text = self.normalize_ascii_vi(text)
        text = self.expand_date_time(text)
        text = self.collapse_whitespace(text)
        text = word_tokenize(text, format='text')

        return text

    def remove_underscore_from_word_tokenization(self, text):
        _re = r'(?=[\w]+)_(?=[\w]+)'
        text= re.sub(_re, ' ', text, 0, re.MULTILINE)
        return text
    
    def clean_text_post_candidates(self, text):
        text = self.remove_underscore_from_word_tokenization(text)
        text = self.expand_roman_numbers(text)
        text = self.expand_measurement_units(text)
        text = self.expand_currency(text)
        text = self.expand_acronyms(text)
        text = self.expand_versioning(text)
        text = self.expand_number(text)
        text = self.change_bon_to_tu(text)
        text = self.expand_abbreviations(text)
        text = self.expand_letter(text)
        text = self.collapse_whitespace(text)
        text = self.lowercase(text)

        return text
    
    def clean(self, text):
        text = self.clean_text_pre_candidates(text)
        if not self.ignore_ambiguity:
            text = self.clean_with_ambiguity(text)
        text = self.clean_text_post_candidates(text)
        return text

    def split_sentences(self, text=None, maxLength=DEFAULT_PIECE_MAX_LENGTH):
        text = text if (text is not None) else self.text
        text = re.sub("(?<![.!?])[\n]+", ".\n", text)
        passages = sent_tokenize(text=text)
        result = []
        breaks = []
        for passage in passages:
            temp = get_pieces(passage, maxLength)
            result += temp
            if len(breaks) > 0:
                breaks += [breaks[-1]+len(temp)]
            else:
                breaks += [len(temp)]
        return result, breaks[0:len(breaks)-1]

    def split_passages(self, text=None, maxLength=DEFAULT_SENTENCE_MAX_LENGTH):
        text = text if (text is not None) else self.text
        passages = split_text_passages(text, r'[\n]+', False, "\n\t ")
        sub_passages = split_long_passages(passages, maxLength)

        combined_sub_passages = [combine_passages(
            i, maxLength) for i in sub_passages]
        sub_passages_lens = [len(i) for i in combined_sub_passages]
        breaks = [sum(sub_passages_lens[:i+1])
                  for i in range(len(sub_passages_lens))]
        flat_list = []

        for sublist in combined_sub_passages:
            for item in sublist:
                flat_list.append(item)
        result = combine_passages(flat_list, maxLength)
        return result, breaks