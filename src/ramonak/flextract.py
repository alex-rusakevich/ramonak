from os.path import commonprefix
from pathlib import Path
from typing import List

import bs4


def find_suffixes(words) -> List[str]:
    common_prefix = commonprefix(words)
    suffixes = []

    if common_prefix == "":
        return

    for word in words:
        if word == common_prefix:
            continue

        if len(common_prefix) - len(word) == 1:
            continue

        suffixes.append(word[len(common_prefix) :])

    return suffixes


def extract_suffixes(ncorp_xml_path) -> List[str]:
    text = Path(ncorp_xml_path).read_text(encoding="utf8")

    print("File is read in memory")

    soup = bs4.BeautifulSoup(text, "xml")

    print("File is processed by bs4")

    suffixes_in_file = []

    for variant in soup.find_all("Variant"):
        print("Processed variant", variant.attrs["lemma"])

        forms = []

        for form in variant.find_all("Form"):
            forms.append(form.text.replace("+", ""))

        suffixes_in_file.extend(find_suffixes(forms))

    suffixes_in_file = filter(lambda x: len(x) <= 3, suffixes_in_file)
    suffixes_in_file = list(set(suffixes_in_file))

    return suffixes_in_file
