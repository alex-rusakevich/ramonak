from pathlib import Path

from ramonak.flextract import extract_flexions
from ramonak.packages.actions import install as rm_install, package_path as rm_pkg_path

rm_install("@bnkorpus/grammar_db/20230920")

flexions = extract_flexions(Path(rm_pkg_path("@bnkorpus/grammar_db/20230920"), "A1.xml"))

print("Знойдзена", len(flexions), "суфіксаў")
print(flexions)
