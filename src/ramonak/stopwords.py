import re
from collections.abc import Iterable

from ramonak.packages.actions import require

STOP_WORDS = (
    (require("@alerus/stopwords") / "belarusian.txt")
    .read_text(encoding="utf8")
    .split("\n")
)


def clean_stop_words(data: str | Iterable[str]) -> str | Iterable[str]:
    if isinstance(data, str):
        for word in STOP_WORDS:
            data = re.sub(rf"\b{word}\b", "", data)

        data = re.sub(r" {2,}", " ", data)
        data = data.strip()
    else:
        word_list = []

        for data_word in data:
            if isinstance(data_word, str):
                msg = f"Wrong type: {type(data_word).__name__}. Data must be str or an iterable with str"
                raise TypeError(msg)

            if data_word not in STOP_WORDS:
                word_list.append(data_word)

        data = word_list

    return data
