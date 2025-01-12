from ramonak.packages.actions import remove
from ramonak.stemmer import FlexionStatStemmer

stemmer = FlexionStatStemmer()


while True:
    word = input("Word to stem: ")

    if word == "exit":
        break

    print(stemmer.stem_word(word))
