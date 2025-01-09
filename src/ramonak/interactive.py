from ramonak.flextract import extract_suffixes

suffixes = extract_suffixes("ncorp/A1.xml")

print("Знойдзена", len(suffixes), "суфіксаў")
print(suffixes)
