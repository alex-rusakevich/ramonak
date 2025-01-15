"""Праца са знакамі прыпынку."""

import re
import string
from collections.abc import Iterable

WORD_PUNCT = string.punctuation + "…"
re_word_punct = re.compile(rf"[{re.escape(WORD_PUNCT)}]")

SENT_PUNCT = ".?!…"


def remove_punct(data: Iterable[str]) -> Iterable[str]:
    """Выдаліць знакі пунктуацыі са спісу радкоў.

    Parameters
    ----------
    data : Iterable[str]
        спіс радкоў

    Returns
    -------
    Iterable[str]
        спіс радкоў без знакаў пунктуацыі

    Raises
    ------
    TypeError
        няправільны тып дадзеных у ``data``
    """
    word_list = []

    if isinstance(data, str):
        msg = f"Wrong type: {type(data).__name__}. Data must be str or an iterable with str"
        raise TypeError(msg)

    for data_word in data:
        if not isinstance(data_word, str):
            msg = f"Wrong type: {type(data_word).__name__}. Data must be str or an iterable with str"
            raise TypeError(msg)

        if not re_word_punct.search(data_word):
            word_list.append(data_word)

    return word_list
