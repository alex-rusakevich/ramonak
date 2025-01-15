"""Модуль з функцыямі для працы з чаргаваннямі і іншымі асаблівасцямі беларускай мовы."""

import re


def unify_dz_ts_to_d_t(word: str) -> str:
    """Ператварыць "дз" і "ц" у "д" і "т".

    Parameters
    ----------
    word : str
        слова для апрацоўкі

    Returns
    -------
    str
        слова без дзекання і цекання
    """
    vowel_pairs = {
        "е": "э",
        "ё": "о",
        "ю": "у",
        "я": "а",
        "і": "ы",
    }

    for jvowel, vowel in vowel_pairs.items():
        word = re.sub("дз" + jvowel, "д" + vowel, word, flags=re.IGNORECASE)
        word = re.sub("ц" + jvowel, "т" + vowel, word, flags=re.IGNORECASE)

        word = re.sub("дзв" + jvowel, "дв" + vowel, word, flags=re.IGNORECASE)
        word = re.sub("цв" + jvowel, "тв" + vowel, word, flags=re.IGNORECASE)

    return word


def fix_trailing_u_short(word: str) -> str:
    """Ператварае "ў" у пачатку слова ў "у".

    Parameters
    ----------
    word : str
        слова для апрацоўкі

    Returns
    -------
    str
        слова з "у" ў пачатку
    """
    return re.sub(r"^ў", "у", word, flags=re.IGNORECASE)


def fix_lang_phenomenons(word: str) -> str:
    """Прымяніць функцыі для ўніфікацыі чаргаванняў і іншых з'яў беларускай мовы.

    Parameters
    ----------
    word : str
        слова для апрацоўкі

    Returns
    -------
    str
        уніфіцыраванае слова
    """
    # region dzekannie, tsekannie, soft + jvowel = hard + jvowel
    word = unify_dz_ts_to_d_t(word)
    # endregion

    return fix_trailing_u_short(word)
