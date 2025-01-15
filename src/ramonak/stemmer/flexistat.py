"""Модуль са стэмерам на аснове статыстыкі флексій."""

from ramonak.packages.actions import require
from ramonak.rules import fix_lang_phenomenons
from ramonak.stemmer.base import BaseStemmer


class FlexionStatStemmer(BaseStemmer):
    """Стэмер на аснове статыстыкі флексій."""

    def __init__(self):
        flexistat_dir = require("@alerus/flexistat_data")

        self.unchangeable_words = []
        self.flexions = []

        with open(
            flexistat_dir / "all_unchangeable.txt",
            encoding="utf8",
        ) as f:
            for unchangealbe_word in f.readlines():
                word = unchangealbe_word.strip()

                if word:
                    self.unchangeable_words.append(word)

        with open(
            flexistat_dir / "all_flexions.txt",
            encoding="utf8",
        ) as f:
            for file_flexion in f.readlines():
                flexion = file_flexion.strip()

                if flexion:
                    self.flexions.append(flexion)

    def stem_word(self, word: str) -> str:
        """Апрацаваць слова стэмерам на аснове алгарытма статыстыкі флексій.

        Parameters
        ----------
        word : str
            слова, якое трэба апрацаваць

        Returns
        -------
        str
            слова, якое было апрацавана стэмерам
        """
        if word in self.unchangeable_words:
            return word

        word = fix_lang_phenomenons(word)

        for flexion in self.flexions:
            if word.endswith(flexion):
                return word[: -len(flexion)]

        return word
