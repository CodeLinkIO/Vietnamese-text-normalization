import re

_percent_re = re.compile(r"([ ]?[%])")
_url_re = re.compile(r"([a-zA-Z])\.(com|gov|org|vn|com.vn|edu.vn)")


_abbreviations_vi = {
    "v\.v": " vân vân. ",
    "v/v": "về việc",
    "đ/c": "địa chỉ",
    "k/g": "kính gửi",
    "th/g": "thân gửi",
    "ko": "không",
    "bit": "biết",
    "bik": "biết",
}

def _expand_percent_vi(m):
    return " phần trăm"


def _expand_urls_vi(m):
    return f"{m.group(1)} chấm {m.group(2)}"

def normalize_abbreviations_vi(text):
    text = normalize_speacial_symbol_vi(text)
    text = re.sub(_url_re, _expand_urls_vi, text)
    for k, v in _abbreviations_vi.items():
        text = re.sub(r"\b" + k + r"\b", v, text, flags=re.IGNORECASE)
    return text


def normalize_speacial_symbol_vi(text):
    text = re.sub(_percent_re, _expand_percent_vi, text)
    text = re.sub("&", " và ", text)
    text = re.sub("@", " a còng ", text)
    text = re.sub("\+", " cộng ", text)
    text = re.sub("//", " xuyệt ", text)
    return text
