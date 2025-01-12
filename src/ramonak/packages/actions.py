from pathlib import Path

from ramonak import PACKAGES_PATH
from ramonak.packages.nexus import PACKAGES
from ramonak.packages.utils import fetch_unzip, package_basic_info, package_exists


def require(wished_package: str) -> None:
    print(f"Required package '{wished_package}'...", end=" ")

    if package_exists(wished_package):
        print("OK")
        return
    else:
        print("Downloading...")

    package_author, package_name, package_version = package_basic_info(wished_package)

    file_url = PACKAGES[package_author][package_name][package_version]

    fetch_unzip(
        file_url,
        Path(PACKAGES_PATH, package_author, package_name, str(package_version)),
    )

    print(
        f"The package '{package_author}/{package_name}/{package_version}' has been installed successfully"
    )
