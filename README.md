# Ramonak

[![CI](https://github.com/alex-rusakevich/ramonak/actions/workflows/ci.yml/badge.svg)](https://github.com/alex-rusakevich/ramonak/actions/workflows/ci.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/ramonak.svg)](https://pypi.org/project/ramonak)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ramonak.svg)](https://pypi.org/project/ramonak)

Універсальная бібліятэка па працы з тэкстам на беларускай мове для Python.

## Як усталяваць?

Напішыце ў вашым тэрмінале:

```sh
pip install ramonak
```

Або ў Google Colab:

```sh
!pip install ramonak
```

## Як карыстацца?

```python
!pip install ramonak -U

import ramonak
from ramonak.tokenizer import word_tokenize
from ramonak.stemmer import FlexionStatStemmer
from ramonak.stopwords import clean_stop_words
from ramonak.punct import remove_punct


text = "Яны iшлi ўдвух выкатанаю нячутна-пругкiмi веласiпедамi сцежкаю ля шэрых нямогла нахiленых да вулiцы платоў...".lower()
tokens = remove_punct(word_tokenize(text))
tokens = clean_stop_words(tokens)

stemmer = FlexionStatStemmer()
print(
      stemmer.stem_words(tokens)
    )
```

Больш падрабязную дакументацыю вы можаце знайсці на сайце https://alex-rusakevich.github.io/ramonak/.

## Дарожная карта

 - [x] Такенізацыя па словам
 - [x] Такенізацыя сказаў
 - [x] Спісак стоп-слоў
 - [x] Просты стэмер, заснаваны на статыстыцы флексій
 - [x] Менеджар пакетаў з дадзенымі
 - [ ] Стэмер Портэра
 - [ ] Леммацізатар
 - [ ] Марфалагічны аналізатар
