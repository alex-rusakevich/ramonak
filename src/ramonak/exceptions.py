"""Модуль з класамі выключэнняў."""


class RamonakError(Exception):
    """Базавы клас для ўсіх выключэнняў ramonak."""


class RamonakPackageManagerError(RamonakError):
    """Агульны клас для ўсіх выключэнняў менеджара пакетаў."""
