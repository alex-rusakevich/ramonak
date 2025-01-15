"""Праца са стоп-словамі."""

from collections.abc import Iterable

from ramonak.packages.actions import require

_stop_words = None


def get_stop_words() -> list[str]:
    """Атрымаць спіс стоп-слоў.

    Returns
    -------
    list[str]
        спіс стоп-слоў
    """
    global _stop_words  # noqa: PLW0603

    if _stop_words:
        return _stop_words

    _stop_words = (require("@alerus/stopwords") / "belarusian.txt").read_text(encoding="utf8").split("\n")
    return _stop_words


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

        if data_word not in get_stop_words():
            word_list.append(data_word)

    return word_list
