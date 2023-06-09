import re
from .letter_vi import spell_letters

acronyms_exceptions_vi = {
    "CĐV": "cổ động viên",
    "CFO": "xi ép ô",
    "CEO": "xi i ô",
    "CTO": "xi ti ô",
    "IQ": "ai kiu",
    "EQ": "i kiu",
    "BBC": "bi bi xi",
    "NBC": "en bi xi",
    "TV": "ti vi",
    "HĐND": "hội đồng nhân dân",
    "TAND": "toàn án nhân dân",
    "BHXH": "bảo hiểm xã hội",
    "BHTN": "bảo hiểm thất nghiệp",
    "TP.HCM": "thành phố hồ chí minh",
    "VN": "việt nam",
    "BCHTW": "ban chấp hành trung ương",
    "ĐT": "đường tỉnh",
    "QL": "quốc lộ",
    "UBND": "uỷ ban nhân dân",
    "TPHCM": "thành phố hồ chí minh",
    "TP": "thành phố",
    "TPCT": "thành phố cần thơ",
    "HCM": "hồ chí minh",
    "SG": "Sài Gòn",
    "HN": "hà nội",
    "BTC": "ban tổ chức",
    "CLB": "câu lạc bộ",
    "HTX": "hợp tác xã",
    "NXB": "nhà xuất bản",
    "ÔBA": "ông bà",
    "QLTT": "quản lý thị trường",
    "BST": "bộ sưu tập",
    "TTTM": "trung tâm thương mại",
    " TT ": " thủ tướng ",
    "TW": "trung ương",
    "GD-ĐT": "giáo dục và đào tạo",
    "BCH": "bản chấp hành",
    "CHXHCNVN": "cộng hòa xã hội chủ nghĩa việt nam",
    "CSGT": "cảnh sát giao thông",
    "MTDTGPMNVN": "mặt trận dân tộc giải phóng miền nam Việt Nam",
    "QDND": "quân đội nhân dân",
    "QLVNCH": "quân lực việt nam cộng hòa",
    "VNCH": "việt nam cộng hòa",
    "LHQ": "liên hợp quốc",
    "UBKT": "uỷ ban kinh tế",
    "THCS": "trung học cơ sở",
    "THPT": "trung học phổ thông",
    "THPTQG": "trung học phổ thông quốc gia",
    "ĐH": "đại học",
    "HLV": "huấn luyện viên",
    "PGS.": "phó giáo sư",
    "PGS": "phó giáo sư",
    "P.GS.": "phó giáo sư",
    "P.GS": "phó giáo sư",
    "GS.": "giáo sư",
    "GS": "giáo sư",
    "ThS.": "thạc sĩ",
    "ThS": "thạc sĩ",
    "TS.": "tiến sĩ",
    "TS": "tiến sĩ",
    "TNHH": "trách nhiệm hữu hạn",
    "CSKH": "chăm sóc khách hàng",
    "VĐV": "vận động viên",
    "NSND": "nghệ sĩ nhân dân",
    "NSƯT": "nghệ sĩ ưu tú",
    "PCCC": "phòng cháy chữa cháy",
    "PGĐ": "phó giám đốc",
    "GĐ": "giám đốc",
    "TPHCM": "thành phố hồ chí minh",
    "BS": "bác sỹ",
    "GDP": "gi đi pi",
    "FDI": "ép đê i",
    "ODA": "ô đê a",
    "VKSND": "viện kiểm soát nhân dân",
    "HĐXX": "hội đồng xét xử",
    "TTXVN": "thông tấn xã việt nam",
    "F và B": "ép èn bi",
    "1-0-2": "một không hai",
    "SN": "sinh năm",
    "môtô": "mô tô",
    "ôtô": "ô tô",
    "êkip": "ê kíp",
    "youtube": "du túp",
    "facebook": "phây búc",
    "tiktok": "tíc tót",
    "KQXS": "kết quả sổ xố",
    "XSMB": "xổ số miền bắc",
    "XSMN": "xổ số miền nam",
    "XSMT": "xổ số miền tây",
    "sars-cov":"sát cô vi",
    "covid":"cô vít",
    "coronavirus": "cô rô na vai rớt"
}

non_uppercase_exceptions = {
    "email": "e-mail",
}

# must ignore roman numerals
_acronym_re = re.compile(r'\b(?:[\d]*[a-z]*[A-Z]\&{0,1}[a-z]*[\d]*){2,}')

    

def expand_acronyms_vi(text):
    for k, v in acronyms_exceptions_vi.items():
        text = re.sub(r"\b" + k + r"\b", v, text, flags=re.IGNORECASE)
    return text

def spell_acronyms_vi(text):
    text = expand_acronyms_vi(text)
    text = re.sub(_acronym_re, spell_letters, text)
    return text