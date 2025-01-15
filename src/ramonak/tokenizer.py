import itertools
import re

from ramonak.punct import SENT_PUNCT, WORD_PUNCT

re_word_tokenize = re.compile(rf"[{re.escape(WORD_PUNCT)}]+")
re_word_tokenize_keep = re.compile(rf"([{re.escape(WORD_PUNCT)}]+)")

re_sent_tokenize_keep = re.compile(r"([^{sent_punct}]+[{sent_punct}]+)".format(sent_punct=re.escape(SENT_PUNCT)))


def word_tokenize(text: str) -> list[str]:
    """Разбіць тэкст на спіс слоў і знакаў прыпынку

    :param text: тэкст, які будзе разбівацца
    :type text: str
    :return: спіс са словамі і знакамі прыпынку
    :rtype: list[str]
    """

    return list(itertools.chain(*[sent_parts.split() for sent_parts in re_word_tokenize_keep.split(text)]))


def sent_tokenize(text: str) -> list[str]:
    """Разбіць тэкст на сказы. Знакі прыпынку захоўваюцца

    :param text: тэкст, які трэба разбіць
    :type text: str
    :return: спіс сказаў
    :rtype: list[str]
    """

    result = []

    for re_sentence in re_sent_tokenize_keep.split(text):
        sentence = re_sentence.strip()

        if not sentence:
            continue

        result.append(sentence)

    return result
