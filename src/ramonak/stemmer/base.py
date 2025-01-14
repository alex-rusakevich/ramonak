class Stemmer:
    def stem_word(self, word):
        raise NotImplementedError

    def stem_words(self, words: list[str]) -> list[str]:
        return [self.stem_word(word) for word in words]
