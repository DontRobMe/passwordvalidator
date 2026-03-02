from typing import Callable, Tuple, List
import re

Rule = Callable[[str], Tuple[bool, str]]


# ============================================================================
# RÈGLES STRICTES (doivent toujours être respectées)
# ============================================================================

def min_length_rule(min_length: int = 8) -> Rule:
    def rule(password: str) -> Tuple[bool, str]:
        return (
            len(password) >= min_length,
            f"Le mot de passe doit contenir au moins {min_length} caractères."
        )
    return rule


def max_length_rule(max_length: int = 20) -> Rule:
    def rule(password: str) -> Tuple[bool, str]:
        return (
            len(password) <= max_length,
            f"Le mot de passe ne doit pas dépasser {max_length} caractères."
        )
    return rule


def no_space_rule(password: str) -> Tuple[bool, str]:
    return (
        not re.search(r"\s", password),
        "Le mot de passe ne doit pas contenir d'espaces."
    )


def no_consecutive_identical_rule(max_consecutive: int = 3) -> Rule:
    def rule(password: str) -> Tuple[bool, str]:
        pattern = rf"([a-zA-Z0-9])\1{{{max_consecutive},}}"
        return (
            not re.search(pattern, password),
            f"Le mot de passe ne doit pas contenir plus de {max_consecutive} caractères identiques consécutifs."
        )
    return rule


def no_common_password_rule(common_passwords: List[str]) -> Rule:
    common_passwords_lower = [p.lower() for p in common_passwords]

    def rule(password: str) -> Tuple[bool, str]:
        return (
            password.lower() not in common_passwords_lower,
            "Le mot de passe est trop commun."
        )
    return rule


# ============================================================================
# RÈGLES DE CARACTÉRISTIQUES (tolérance possible)
# ============================================================================

def uppercase_rule(password: str) -> Tuple[bool, str]:
    return (
        bool(re.search(r"[A-Z]", password)),
        "Le mot de passe doit contenir une majuscule."
    )


def lowercase_rule(password: str) -> Tuple[bool, str]:
    return (
        bool(re.search(r"[a-z]", password)),
        "Le mot de passe doit contenir une minuscule."
    )


def number_rule(password: str) -> Tuple[bool, str]:
    return (
        bool(re.search(r"[0-9]", password)),
        "Le mot de passe doit contenir un chiffre."
    )


def special_char_rule(password: str) -> Tuple[bool, str]:
    return (
        bool(re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password)),
        "Le mot de passe doit contenir un caractère spécial."
    )

