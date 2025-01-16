"""Фунцыі кіравання пакетамі."""

import shutil
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import cast

from ramonak import PACKAGES_PATH
from ramonak.exceptions import RamonakPackageManagerError
from ramonak.packages import HERBARIUM_PATH
from ramonak.packages._utils import (
    _fetch_unzip,
    _get_package_id_parts,
    _get_package_versions,
    _local_package_exists,
    _retrieve_package_url,
)


def require(package_id: str) -> Path:
    """Падключыць да кода пакет з дадзенымі. Калі гэтага пакета няма, ён будзе спампаваны.

    Parameters
    ----------
    package_id : str
        id пакета, напрыклад, ``@alerus/stopwords``. Імя састаіць
        з кода аўтара і імя пакета

    Returns
    -------
    Path
        шлях да папкі, куды пакет быў усталяваны. Файламі адтуль можна
        карыстацца з дапамогай ``/``

    Examples
    --------
    .. code-block:: python
        :linenos:

        package = require("@author/package")
        f = open(package / "file.txt", "r", encoding="utf8")
    """
    package_author, package_name, package_version = _get_package_id_parts(package_id)

    if "==" not in package_id:
        package_version = _get_package_versions(package_author, package_name)[-1]["id"]
        print(
            f"Required '{package_id}=={package_version}'...",
            end=" ",
        )
    else:
        print(f"Required package '{package_id}'...", end=" ")

    sys.stdout.flush()

    package_path = Path(PACKAGES_PATH, package_author, package_name, str(package_version)).resolve()

    if package_version == "git":
        git_path = shutil.which("git")

        if _local_package_exists(package_id if "==" in package_id else package_id + "==" + package_version):
            if (
                subprocess.run(
                    [cast(str, git_path), "-C", str(package_path), "pull"],
                    stdout=sys.stdout,
                    stderr=sys.stderr,
                    check=False,
                ).returncode
                != 0
            ):
                msg = "Git failed with an error"
                raise RamonakPackageManagerError(msg)

            return package_path

        print("Downloading...")

        file_url = _retrieve_package_url(package_author, package_name, package_version)
        package_path.mkdir(parents=True, exist_ok=True)

        if (
            subprocess.run(
                [cast(str, git_path), "clone", file_url, str(package_path)],
                stdout=sys.stdout,
                stderr=sys.stderr,
                check=False,
            ).returncode
            != 0
        ):
            msg = "Git failed with an error"
            raise RamonakPackageManagerError(msg)
    else:
        if _local_package_exists(package_id if "==" in package_id else package_id + "==" + package_version):
            print("Already satisfied")
            return package_path.resolve()
        print("Downloading...")

        file_url = _retrieve_package_url(package_author, package_name, package_version)

        _fetch_unzip(
            file_url,
            package_path,
        )

    print(f"The package '{package_author}/{package_name}=={package_version}' has been installed successfully")

    return package_path


def remove(package_id: str):
    """Выдаліць пакет з лакальнага сховішча.

    Parameters
    ----------
    package_id : str
        id пакета у фармаце ``@author/package``. Можна
        таксама ўказаць канкрэтны нумар версіі, дабавіўшы ў канцы
        ``==version_number``. Без гэтага азначэння будуць выдалены ўсе версіі
        пакета

    Raises
    ------
    RamonakPackageManagerError
        няправільнае імя пакета або пакет не існуе

    Examples
    --------
    .. code-block:: python
        :linenos:

        remove("@alerus/package")  # выдаліць усе версіі пакета
        remove("@alerus/package==123")  # выдаліць пакет з версіяй ``123``
    """
    removable_path: Path | str = ""

    author, name, version = _get_package_id_parts(package_id)

    if "==" not in package_id:
        print(
            f"Removing the local metapackage '{author}/{name}'...",
            end=" ",
        )
        removable_path = Path(PACKAGES_PATH, author, name)
    else:
        print(
            f"Removing the local package '{author}/{name}=={version}'...",
            end=" ",
        )
        removable_path = Path(PACKAGES_PATH, author, name, version)

    try:
        shutil.rmtree(removable_path)
    except FileNotFoundError as err:
        msg = "The package doesn't exist in the local storage"
        raise RamonakPackageManagerError(msg) from err
    else:
        print("OK")


def purge():
    """Выдаліць *усе* пакеты з лакальнага сховішча."""
    print("Removing all the local packages...", end=" ")

    shutil.rmtree(PACKAGES_PATH)
    PACKAGES_PATH.mkdir(parents=True)

    print("OK")


def info(package_id: str):
    """Вывесці інфармацыю пра пакет.

    Parameters
    ----------
    package_id : str
        id пакета у фармаце ``@author/package``
        або ``@author/package==version``
    """
    author, name, version = _get_package_id_parts(package_id)
    package_file = str(Path(HERBARIUM_PATH, author, name)) + ".toml"
    descriptor_text = Path(package_file).read_text(encoding="utf8")
    descriptor_data = tomllib.loads(descriptor_text)

    if not version:
        print("type", "=", "metapackage")
    else:
        print("type", "=", "package")

    for key, value in descriptor_data["package_info"].items():
        print(key, "=", value)

    if not version:
        versions = ",".join(v["id"] for v in descriptor_data["versions"])
        print(f"versions = [{versions}]")
    else:
        version_dict = next(v for v in descriptor_data["versions"] if v["id"] == version)

        for key, value in version_dict.items():
            print(f"version.{key} = {value}")
