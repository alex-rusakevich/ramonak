from collections.abc import Iterable


class Stemmer:
    def stem_word(self, word):
        raise NotImplementedError

    def stem_words(self, words: Iterable[str]) -> list[str]:
        """Апрацаваць стэмерам кожнае слова ў спісе слоў

        :param words: спіс слоў
        :type words: Iterable[str]
        :return: спіс слоў, якія былі апрацаваны стэмерам
        :rtype: list[str]
        """
        return [self.stem_word(word) for word in words]
