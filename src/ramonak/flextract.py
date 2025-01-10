from os.path import commonprefix
from typing import List, Tuple
from pathlib import Path
from collections import Counter
import gc
from ramonak.packages.actions import package_path as rm_pkg_path

from lxml import etree

from ramonak.packages.actions import install as rm_install


rm_install("@bnkorpus/grammar_db/20230920")


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
        variant_lemma = variant.get("lemma").replace("+", "")
        forms = []

        if "-" in variant_lemma:
            continue

        for form in variant.findall("Form"):
            forms.append(form.text.replace("+", ""))

        flexions = find_flexions((variant_lemma, *forms))
        flexions_in_file.extend(flexions)

    return flexions_in_file


def xml_flexion_stats(xml_dir_path: str) -> Tuple[Tuple[str, int]]:
    all_flexions = []

    for xml_file in Path(xml_dir_path).glob("*.xml"):
        print("Processing", xml_file)
        all_flexions.extend(
                extract_flexions(xml_file)
                )
        gc.collect()

    print("All flexions: {}. Counting total stats...".format(len(all_flexions)))

    flexions_and_count = Counter(all_flexions).items()

    print("Flexions: {}. Sorting...".format(len(flexions_and_count)))

    flexions_and_count = sorted(flexions_and_count, key=lambda x: x[1], reverse=True)

    return flexions_and_count


def get_flexions():
    flexions_and_count = xml_flexion_stats(rm_pkg_path("@bnkorpus/grammar_db/20230920"))
    max_count = flexions_and_count[0][1]

    flexions_and_count = map(lambda x: (x[0], round(x[1]/max_count, 1)), flexions_and_count)
    flexions_and_count = tuple(filter(lambda x: x[1] > 0, flexions_and_count))

    print("Valuable flexions: {}".format(len(flexions_and_count)))

    return tuple(x[0] for x in flexions_and_count)

