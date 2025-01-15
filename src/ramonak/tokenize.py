"""Модуль з функцыямі такенізацыі."""

import itertools
import re

from ramonak.punct import SENT_PUNCT, WORD_PUNCT

re_word_tokenize = re.compile(rf"[{re.escape(WORD_PUNCT)}]+")
re_word_tokenize_keep = re.compile(rf"([{re.escape(WORD_PUNCT)}]+)")

re_sent_tokenize_keep = re.compile(r"([^{sent_punct}]+[{sent_punct}]+)".format(sent_punct=re.escape(SENT_PUNCT)))


def word_tokenize(text: str) -> list[str]:
    """Разбіць тэкст на спіс слоў і знакаў прыпынку.

    Parameters
    ----------
    text : str
        тэкст, які будзе разбівацца

    Returns
    -------
    list[str]
        спіс са словамі і знакамі прыпынку
    """
    return list(itertools.chain(*[sent_parts.split() for sent_parts in re_word_tokenize_keep.split(text)]))


def sent_tokenize(text: str) -> list[str]:
    """Разбіць тэкст на сказы. Знакі прыпынку захоўваюцца.

    Parameters
    ----------
    text : str
        тэкст, які трэба разбіць

    Returns
    -------
    list[str]
        спіс сказаў
    """
    result = []

    for re_sentence in re_sent_tokenize_keep.split(text):
        sentence = re_sentence.strip()

        if not sentence:
            continue

        result.append(sentence)

    return result
