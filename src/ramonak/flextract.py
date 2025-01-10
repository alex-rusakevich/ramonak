from os.path import commonprefix
from typing import List

from lxml import etree


def find_flexions(words) -> List[str]:
    common_prefix = commonprefix(words)
    flexions = []

    if common_prefix == "":
        return flexions

    for word in words:
        if word == common_prefix:
            continue

        if len(common_prefix) - len(word) == 1:
            continue

        flexions.append(word[len(common_prefix):])

    return flexions


def extract_flexions(ncorp_xml_path) -> List[str]:
    f = etree.parse(ncorp_xml_path)
    root = f.getroot()

    print("File has been loaded in lxml")

    flexions_in_file = []

    for variant in root.findall("Paradigm/Variant"):
        forms = []

        for form in variant.findall("Form"):
            form_content = form.text.replace("+", "")

            if "-" in form_content:
                continue

            forms.append(form.text.replace("+", ""))

        flexions = find_flexions(forms)
        flexions_in_file.extend(flexions)

    print("Flexions were found. Counting...")

    # flexions_in_file = filter(lambda x: len(x) <= 3, flexions_in_file)
    flexions_count = []

    for flexion in set(flexions_in_file):
        flexions_count.append(
                (flexion, flexions_in_file.count(flexion))
                )

    flexions_count = sorted(flexions_count, key=lambda x: x[1], reverse=True)

    print(flexions_count)

    return set(flexions_in_file)
