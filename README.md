# vi_cleaner

ViCleaner is a Python library for normalizing Vietnamese text for CodeLink's text to speech API.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install vi_cleaner with Github link.

```bash
pip install git+https://github.com/CodeLinkIO/Vietnamese-text-normalization.git@main
```

## Usage
### 1. Normalize Vietnamese text
```python
from vi_cleaner.vi_cleaner import ViCleaner
text = "Ngày 01/02 là ngày mùng 1 Tết , tôi thêm 1 tuổi mới,cao thêm 3 cm, được lì xì 1.000.000 đồng."

# 1. Normalize text passed to the cleaner
cleaner = ViCleaner(text)
print(cleaner.clean())
# Output: ngày một tháng hai là ngày mùng một tết, tôi thêm một tuổi mới, cao thêm ba xen ti mét, được lì xì một triệu đồng.

# 2. Normalize text passed as an argument
print(cleaner.clean_text(text))
# Output: ngày một tháng hai là ngày mùng một tết, tôi thêm một tuổi mới, cao thêm ba xen ti mét, được lì xì một triệu đồng.

# 3. Join lines
text = "Một\nhai\nba"
print(cleaner.join_lines(text))
# Output: một hai ba
```

### 2. Split passage (to sentences)

### 3. Split sentence (to pieces)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
//