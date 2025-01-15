"""Галоўны модуль праекта. Грузіць .env-файлы, стварае неабходныя папкі."""

import os
from pathlib import Path
from typing import cast

from dotenv import dotenv_values

os.environ.update(cast(dict[str, str], dotenv_values(".env.dev")))
os.environ.update(cast(dict[str, str], dotenv_values(".env.prod")))

RAMONAK_PATH = Path(
    os.environ.get("RAMONAK_PATH", os.path.join(os.path.expanduser("~"), ".alerus", "ramonak"))
).resolve()

PACKAGES_PATH = Path(RAMONAK_PATH, "packages").resolve()

for path in (RAMONAK_PATH, PACKAGES_PATH):
    path.mkdir(parents=True, exist_ok=True)
