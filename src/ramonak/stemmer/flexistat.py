from ramonak.packages.actions import require
from ramonak.rules import fix_lang_phenomenons
from ramonak.stemmer.base import Stemmer


class FlexionStatStemmer(Stemmer):
    def __init__(self):
        flexistat_dir = require("@alerus/flexistat_data")

        self.unchangeable_words = []
        self.flexions = []

        with open(
            flexistat_dir / "unchangeable_words.txt",
            encoding="utf8",
        ) as f:
            for unchangealbe_word in f.readlines():
                word = unchangealbe_word.strip()

                if word:
                    self.unchangeable_words.append(word)

        with open(
            flexistat_dir / "flexions.txt",
            encoding="utf8",
        ) as f:
            for file_flexion in f.readlines():
                flexion = file_flexion.strip()

                if flexion:
                    self.flexions.append(flexion)

    def stem_word(self, word: str) -> str:
        if word in self.unchangeable_words:
            return word

        word = fix_lang_phenomenons(word)

        for flexion in self.flexions:
            if word.endswith(flexion):
                return word[: -len(flexion)]

        return word
