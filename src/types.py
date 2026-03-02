from dataclasses import dataclass, field
from enum import Enum
from typing import List, Callable, Tuple

Rule = Callable[[str], Tuple[bool, str]]


class PasswordStrength(Enum):
    INVALID = "invalid"
    WEAK = "weak"
    MEDIUM = "medium"
    STRONG = "strong"


@dataclass
class ValidationResult:
    is_valid: bool
    strength: PasswordStrength
    errors: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "valid": self.is_valid,
            "strength": self.strength.value,
            "errors": self.errors
        }


@dataclass
class ValidationConfig:
    min_length: int = 8
    max_length: int = 20
    max_consecutive: int = 3
    characteristic_tolerance: int = 1
    common_passwords: List[str] = field(default_factory=lambda: [
        "password", "123456", "12345678", "qwerty", "abc123",
        "password123", "admin", "letmein", "welcome", "monkey",
        "dragon", "master", "123456789", "1234567", "solo"
    ])

