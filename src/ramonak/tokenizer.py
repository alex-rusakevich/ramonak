import itertools
import re
import string

word_punct = string.punctuation + "…"
sent_punct = ".?!…"

re_word_tokenize = re.compile(rf"[{re.escape(word_punct)}]+")
re_word_tokenize_keep = re.compile(rf"([{re.escape(word_punct)}]+)")

re_sent_tokenize_keep = re.compile(
    r"([^{sent_punct}]+[{sent_punct}]+)".format(sent_punct=re.escape(sent_punct))
)


def word_tokenize(text: str, remove_punct: bool = False) -> list[str]:
    regex = re_word_tokenize_keep

    if remove_punct:
        regex = re_word_tokenize

    result = [sent_parts.split() for sent_parts in regex.split(text)]

    return list(itertools.chain(*result))


def sent_tokenize(text: str) -> list[str]:
    result = []

    for re_sentence in re_sent_tokenize_keep.split(text):
        sentence = re_sentence.strip()

        if not sentence:
            continue

        result.append(sentence)

    return result
