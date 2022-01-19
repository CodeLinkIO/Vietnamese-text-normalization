import re
import unicodedata

from .letter_vi import normalize_letter_vi
from .currency_vi import normalize_currency_vi
from .acronym_vi import spell_acronyms_vi
from .numberical_vi import normalize_number_vi
from .measurement_vi import normalize_measurement_vi
from .datestime_vi import normalize_date, normalize_time
from .roman_number_vi import normalize_roman_numbers
from .abbreviation_vi import normalize_abbreviations_vi
from .symbol_vi import opening_brackets_and_punctutations_re, punctutations_re


class ViCleaner(object):
    def __init__(self, text):
        text = self.collapse_whitespace(text)
        self.text = " " + text + " "

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
        text = re.sub(punctutations_re, self._collapse_whitespace_before_punctuation, text)
        text = re.sub(opening_brackets_and_punctutations_re, self._collapse_whitespace_after_bracket, text)
        text = re.sub(r"(\s)\1{1,}", r"\1", text)
        text = re.sub(r"\t+", " ", text)
        text = text.strip()
        return text

    def lowercase(self, text):
        return text.lower()

    def clean_basic(self,text):
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
        text = normalize_date(text)
        text = normalize_time(text)
        return text

    def expand_measurement_units(self, text):
        return normalize_measurement_vi(text)

    def expand_currency(self, text):
        return normalize_currency_vi(text)

    def expand_number(self, text):
        return normalize_number_vi(text)

    def expand_letter(self, text):
        return normalize_letter_vi(text)

    def normalize_splash(self, text):
        text = re.sub(r"(/)", " trên ", text)
        return text

    def remove_left_hyphen(self, text):
        return re.sub(r"([^\s])(-)([^\s])", r"\1 \3", text)

    def clean(self):
        self.text = self.normalize_ascii_vi(self.text)
        self.text = self.expand_abbreviations(self.text)
        self.text = self.expand_roman_numbers(self.text)
        self.text = self.expand_acronyms(self.text)
        self.text = self.expand_date_time(self.text)
        self.text = self.expand_measurement_units(self.text)
        self.text = self.expand_currency(self.text)
        self.text = self.expand_number(self.text)
        self.text = self.expand_letter(self.text)
        self.text = self.normalize_splash(self.text)
        self.text = self.remove_left_hyphen(self.text)

        self.text = self.collapse_whitespace(self.text)
        self.text = self.lowercase(self.text)
        return self.text

    def clean_text(self, text):
        text = self.collapse_whitespace(text)
        text = " " + text + " "

        text = self.normalize_ascii_vi(text)
        text = self.expand_abbreviations(text)
        text = self.expand_roman_numbers(text)
        text = self.expand_acronyms(text)
        text = self.expand_date_time(text)
        text = self.expand_measurement_units(text)
        text = self.expand_currency(text)
        text = self.expand_number(text)
        text = self.expand_letter(text)
        text = self.normalize_splash(text)
        text = self.remove_left_hyphen(text)

        text = self.collapse_whitespace(text)
        text = self.lowercase(text)
        return text