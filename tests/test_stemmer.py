from ramonak.stemmer.flexistat import FlexionStatStemmer


def test_flexistat_stemmer():
    stemmer = FlexionStatStemmer()

    assert stemmer.stem_words(["лесам", "лесу"]) == (["лес"] * 2)
