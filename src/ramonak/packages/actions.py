from pathlib import Path
import io
import zipfile
import requests
from ramonak import PACKAGES_PATH


def fetch_unzip(zip_file_url: str, destination_dir: str) -> Path:
    Path(destination_dir).mkdir(exist_ok=True, parents=True)

    r = requests.get(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(destination_dir)


def package_exists(package_name: str) -> bool:
    if Path(PACKAGES_PATH, package_name).exists:
        return True
    else:
        return False


def install(package_name: str) -> None:
    print(f"Installing {package_name}...", end=" ")

    if package_exists(package_name):
        print("Package exists, skipping")
        return

    if package_name == "@bnkorpus/grammar_db/20230920":
        fetch_unzip(
                "https://github.com/Belarus/GrammarDB/releases/download/RELEASE-202309/RELEASE-20230920.zip",
                Path(PACKAGES_PATH, package_name)
                )
    else:
        print("Unknown package. Stopping")
        return

    print("OK")


def package_path(package_name: str) -> str:
    return Path(PACKAGES_PATH, package_name)

