"""Праца са стоп-словамі."""

from collections.abc import Iterable

from ramonak.packages.actions import require

STOP_WORDS = (
    (require("@alerus/stopwords") / "belarusian.txt")
    .read_text(encoding="utf8")
    .split("\n")
)


def clean_stop_words(data: Iterable[str]) -> Iterable[str]:
    """Убраць усе стоп-словы са спісу радкоў.

    Parameters
    ----------
    data : Iterable[str]
        спіс радкоў

    Returns
    -------
    Iterable[str]
        спіс радкоў без стоп-слоў

    Raises
    ------
    TypeError
        няправільны тып дадзеных у ``data``
    """
    if isinstance(data, str):
        msg = f"Wrong type: {type(data).__name__}. Data must be str or an iterable with str"
        raise TypeError(msg)

    word_list = []

    for data_word in data:
        if not isinstance(data_word, str):
            msg = f"Wrong type: {type(data_word).__name__}. Data must be str or an iterable with str"
            raise TypeError(msg)

        if data_word not in STOP_WORDS:
            word_list.append(data_word)

    return word_list
