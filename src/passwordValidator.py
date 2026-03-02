import re
from enum import Enum


class PasswordStrength(Enum):
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


class PasswordValidator:
    COMMON_PASSWORDS = {
        "password", "123456", "12345678", "qwerty", "abc123",
        "password123", "admin", "letmein", "welcome", "monkey",
        "dragon", "master", "123456789", "1234567", "solo"
    }

    SPECIAL_CHARS = "@#$%^&+=!"
    MIN_LENGTH = 8
    MAX_LENGTH = 20
    MAX_CONSECUTIVE = 3

    def __init__(self):
        pass

    def validate(self, password: str) -> tuple[bool, list[str]]:
        errors: list[str] = []

        if len(password) < self.MIN_LENGTH:
            errors.append(f"Le mot de passe doit contenir au moins {self.MIN_LENGTH} caractères")
        if len(password) > self.MAX_LENGTH:
            errors.append(f"Le mot de passe ne doit pas dépasser {self.MAX_LENGTH} caractères")

        if " " in password:
            errors.append("Le mot de passe ne peut pas contenir d'espaces")

        if not self._check_consecutive_chars(password):
            errors.append(
                f"Le mot de passe ne peut pas contenir plus de {self.MAX_CONSECUTIVE} "
                f"caractères identiques consécutifs"
            )

        characteristics_count = self._count_characteristics(password)
        if characteristics_count < 3:
            errors.append(
                "Le mot de passe doit contenir au moins 3 des 4 éléments suivants: "
                "majuscule, minuscule, chiffre, caractère spécial"
            )

        if password.lower() in self.COMMON_PASSWORDS:
            errors.append("Ce mot de passe est trop commun")

        return len(errors) == 0, errors

    def _check_consecutive_chars(self, password: str) -> bool:
        for i in range(len(password) - self.MAX_CONSECUTIVE):
            if password[i] == password[i + 1] == password[i + 2] == password[i + 3]:
                return False
        return True

    def _count_characteristics(self, password: str) -> int:
        count = 0
        if re.search(r"[A-Z]", password):
            count += 1
        if re.search(r"[a-z]", password):
            count += 1
        if re.search(r"\d", password):
            count += 1
        if any(char in self.SPECIAL_CHARS for char in password):
            count += 1
        return count

    def get_strength(self, password: str) -> PasswordStrength:
        is_valid, _ = self.validate(password)

        if not is_valid:
            return PasswordStrength.WEAK

        characteristics_count = self._count_characteristics(password)
        length = len(password)

        if characteristics_count < 3:
            return PasswordStrength.WEAK
        if characteristics_count == 3:
            return PasswordStrength.MEDIUM

        if length < 10:
            return PasswordStrength.MEDIUM
        return PasswordStrength.STRONG

    def get_validation_report(self, password: str) -> dict:
        is_valid, errors = self.validate(password)
        strength = self.get_strength(password)

        return {
            "valid": is_valid,
            "errors": errors,
            "strength": strength.value,
            "characteristics": self._count_characteristics(password),
        }
