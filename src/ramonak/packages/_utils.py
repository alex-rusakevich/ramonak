import io
import re
import tomllib
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm

from ramonak import PACKAGES_PATH
from ramonak.exceptions import RamonakPackageManagerError
from ramonak.packages import HERBARIUM_PATH


def _fetch_unzip(zip_file_url: str, destination_dir: Path | str) -> Path:
    Path(destination_dir).mkdir(exist_ok=True, parents=True)
    bio = io.BytesIO()

    response = requests.get(zip_file_url, stream=True, timeout=10)
    with tqdm.wrapattr(
        bio,
        "write",
        miniters=1,
        desc=zip_file_url.split("/")[-1],
        total=int(response.headers.get("content-length", 0)),
    ) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)

    z = zipfile.ZipFile(bio)
    z.extractall(destination_dir)

    return Path(destination_dir)


def _package_path(package_id: str) -> Path:
    author, name, version = _get_package_id_parts(package_id)
    return Path(PACKAGES_PATH, author, name, version)


def _local_package_exists(package_name: str) -> bool:
    package_dir = _package_path(package_name)

    if package_dir.exists() and any(package_dir.iterdir()):
        return True
    return False


def _get_package_id_parts(package: str) -> tuple[str, str, str]:
    package = re.sub(r"\s", "", package)

    package_version = ""
    package_name = ""
    package_author = ""

    if "==" in package:  # Installing exact version
        _, package_version = package.split("==")
        package_author, package_name = package.split("==")[0].split("/")
    elif package.count("/") == 1:  # Get latest version
        package_author, package_name = package.split("/")
    else:
        msg = "Wrong package name. At least author and package name must be present"
        raise RamonakPackageManagerError(msg)

    return package_author, package_name, package_version


def _get_package_versions(package_author, package_name) -> list:
    package_file = str(Path(HERBARIUM_PATH, package_author, package_name)) + ".toml"
    package_dict = tomllib.loads(Path(package_file).read_text(encoding="utf8"))

    return package_dict["versions"]


def _retrieve_package_url(package_author, package_name, package_version) -> str:
    package_file = str(Path(HERBARIUM_PATH, package_author, package_name)) + ".toml"
    package_dict = tomllib.loads(Path(package_file).read_text(encoding="utf8"))

    for version in package_dict["versions"]:
        if version["id"] == package_version:
            return version["url"]

    msg = f"No such package version found: {package_author}/{package_name}=={package_version}"
    raise RamonakPackageManagerError(msg)
