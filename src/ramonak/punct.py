import re
import string
from collections.abc import Iterable

WORD_PUNCT = string.punctuation + "…"
re_word_punct = re.compile(rf"[{re.escape(WORD_PUNCT)}]")

SENT_PUNCT = ".?!…"


def remove_punct(data: str | Iterable[str]) -> str | Iterable[str]:
    print(data)

    if isinstance(data, str):
        data = re_word_punct.sub("", data)
        data = re.sub(r" {2,}", " ", data)

        return data.strip()

    word_list = []

    for data_word in data:
        if not isinstance(data_word, str):
            msg = f"Wrong type: {type(data_word).__name__}. Data must be str or an iterable with str"
            raise TypeError(msg)

        if not re_word_punct.search(data_word):
            word_list.append(data_word)

    return word_list
