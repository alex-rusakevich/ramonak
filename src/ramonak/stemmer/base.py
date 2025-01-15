"""Модуль з базавым класам для ўсіх стэмераў."""

from collections.abc import Iterable


class BaseStemmer:
    """Базавы стэмер. Карыстаецца як прэдак для іншых стэмераў."""

    def stem_word(self, word):
        """Апрацаваць стэмерам адно слова. У класах-наследніках гэта функцыя перавызначана."""
        raise NotImplementedError

    def stem_words(self, words: Iterable[str]) -> list[str]:
        """Апрацаваць стэмерам кожнае слова ў спісе слоў.

        Parameters
        ----------
        words : Iterable[str]
            спіс слоў

        Returns
        -------
        list[str]
            спіс слоў, якія былі апрацаваны стэмерам
        """
        return [self.stem_word(word) for word in words]
