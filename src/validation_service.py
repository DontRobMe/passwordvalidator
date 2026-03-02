from typing import List
from src.types import Rule, ValidationResult, PasswordStrength, ValidationConfig
from src.rules import (
    min_length_rule,
    max_length_rule,
    no_space_rule,
    no_consecutive_identical_rule,
    no_common_password_rule,
    uppercase_rule,
    lowercase_rule,
    number_rule,
    special_char_rule
)


class PasswordValidationService:

    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()
        self._setup_rules()

    def _setup_rules(self) -> None:
        self.strict_rules: List[Rule] = [
            min_length_rule(self.config.min_length),
            max_length_rule(self.config.max_length),
            no_space_rule,
            no_consecutive_identical_rule(self.config.max_consecutive),
            no_common_password_rule(self.config.common_passwords)
        ]

        self.characteristic_rules: List[Rule] = [
            uppercase_rule,
            lowercase_rule,
            number_rule,
            special_char_rule
        ]

    def validate(self, password: str) -> ValidationResult:
        strict_results = [rule(password) for rule in self.strict_rules]
        strict_errors = [msg for ok, msg in strict_results if not ok]

        if strict_errors:
            return ValidationResult(
                is_valid=False,
                strength=PasswordStrength.INVALID,
                errors=strict_errors
            )

        char_results = [rule(password) for rule in self.characteristic_rules]
        successful_checks = sum(1 for ok, _ in char_results if ok)
        char_errors = [msg for ok, msg in char_results if not ok]

        is_valid = successful_checks >= (
            len(self.characteristic_rules) - self.config.characteristic_tolerance
        )
        strength = self._calculate_strength(successful_checks)

        return ValidationResult(
            is_valid=is_valid,
            strength=strength,
            errors=char_errors if not is_valid else []
        )

    def _calculate_strength(self, successful_checks: int) -> PasswordStrength:
        total_rules = len(self.characteristic_rules)

        if successful_checks == total_rules:
            return PasswordStrength.STRONG
        if successful_checks == total_rules - 1:
            return PasswordStrength.MEDIUM
        if successful_checks >= 1:
            return PasswordStrength.WEAK

        return PasswordStrength.INVALID

