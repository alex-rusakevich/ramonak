import re

from ramonak.stemmer.base import Stemmer


class SnowballStemmer(Stemmer):
    # Helper regex strings.
    _vowel = "[аеіоуыэюя]"
    _non_vowel = "[^аеіоуыэюя]"

    # Word regions TODO
    _re_rv = re.compile(_vowel)
    _re_r1 = re.compile(_vowel + _non_vowel)

    # Дзеепрыслоўе прошлага часу закончанага трывання
    _re_perfective_gerund = re.compile(
        r"(((?P<ignore>{vowel})(ўшы|ўшыся))|(шы|шыся))$".format(vowel=_vowel)
    )

    # Канчаткі прыметніка
    _adjective_endings = (
        r"(ы|і|ая|яя|ое|яе|ыя|ія|ага|яга|ай|яй|ых|іх|аму|яму|ым|ім|ымі|імі)"
    )

    # Прыметнік
    _re_adjective = re.compile(
        r"{adjective_endings}$".format(adjective_endings=_adjective_endings)
    )

    # Дзеепрыменік (суфіксы дзеепрыметніка + канчаткі прыметніка)
    _re_participle = re.compile(
        r"((уч|юч|ач|яч|л|ш|ўш|ем|ім|н|ен|ан|т){adjective_endings})$".format(
            adjective_endings=_adjective_endings
        )
    )

    # Зваротныя постфіксы
    _re_reflexive = re.compile(r"(ся|цца|ца|сь)$")

    # Дзеяслоў
    _re_verb = re.compile(
        r"((ыва|іва|ся|іць|аць|ну|о|е)"
        r"|(іш|у|ем|яць|ю|іце|аць|аце|іць|ала|лі|ім|аў|аш))$"
    )

    _re_noun = re.compile(
        r"(а|еў|оў|іе|ье|е|іямі|ямі|амі|еі|іі|і|іей|ей|ой|ій|й|іям|ям|іем|ем|"
        r"ам|ом|о|у|ах|іях|ях|ы|ь|ію|ью|ю|ія|ья|я)$"
    )

    _re_derivational = re.compile(r"(аст|асць)$")

    _re_i = re.compile(r"і$")

    _re_nn = re.compile(r"((?<=н)н)$")

    _re_soft_sign = re.compile(r"ь$")

    def stem_word(self, word):
        """
        Gets the stem.
        """

        rv_pos, r2_pos = self._find_rv(word), self._find_r2(word)
        word = self._step_1(word, rv_pos)
        word = self._step_2(word, rv_pos)
        word = self._step_3(word, r2_pos)
        word = self._step_4(word, rv_pos)
        return word

    def _find_rv(self, word):
        """
        Searches for the RV region.
        """

        rv_match = self._re_rv.search(word)
        if not rv_match:
            return len(word)
        return rv_match.end()

    def _find_r2(self, word):
        """
        Searches for the R2 region.
        """

        r1_match = self._re_r1.search(word)
        if not r1_match:
            return len(word)
        r2_match = self._re_r1.search(word, r1_match.end())
        if not r2_match:
            return len(word)
        return r2_match.end()

    def _cut(self, word, ending, pos):
        """
        Tries to cut the specified ending after the specified position.
        """

        match = ending.search(word, pos)
        if match:
            try:
                ignore = match.group("ignore") or ""
            except IndexError:
                return True, word[: match.start()]
            else:
                return True, word[: match.start() + len(ignore)]
        else:
            return False, word

    def _step_1(self, word, rv_pos):
        match, word = self._cut(word, self._re_perfective_gerund, rv_pos)
        if match:
            return word
        _, word = self._cut(word, self._re_reflexive, rv_pos)
        match, word = self._cut(word, self._re_adjective, rv_pos)
        if match:
            _, word = self._cut(word, self._re_participle, rv_pos)
            return word
        match, word = self._cut(word, self._re_verb, rv_pos)
        if match:
            return word
        _, word = self._cut(word, self._re_noun, rv_pos)
        return word

    def _step_2(self, word, rv_pos):
        _, word = self._cut(word, self._re_i, rv_pos)
        return word

    def _step_3(self, word, r2_pos):
        _, word = self._cut(word, self._re_derivational, r2_pos)
        return word

    def _step_4(self, word, rv_pos):
        match, word = self._cut(word, self._re_nn, rv_pos)
        if not match:
            _, word = self._cut(word, self._re_soft_sign, rv_pos)
        return word
