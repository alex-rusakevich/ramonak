from ramonak.packages.actions import require, remove
import os


def test_require_simple():
    pkg_dir = require("@alerus/stopwords")

    assert len(os.listdir(pkg_dir)) != 0
    

def test_remove_all_of_metapkg():
    pkg_dir = require("@alerus/stopwords")
    remove("@alerus/stopwords")

    assert pkg_dir.exists() != True
