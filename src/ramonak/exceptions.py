"""Модуль з класамі выключэнняў."""


class RamonakError(Exception):
    """Базавы клас для ўсіх выключэнняў ramonak."""

    pass


class RamonakPackageManagerError(RamonakError):
    """Агульны клас для ўсіх выключэнняў менеджэра пакетаў."""

    pass
