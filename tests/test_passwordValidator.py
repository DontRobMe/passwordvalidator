import pytest
from src.passwordValidator import PasswordValidator, PasswordStrength


@pytest.fixture
def validator():
    return PasswordValidator()


class TestPasswordLength:
    def test_password_too_short(self, validator):
        is_valid, errors = validator.validate("Short1!")
        assert not is_valid
        assert any("au moins 8" in error for error in errors)

    def test_password_too_long(self, validator):
        is_valid, errors = validator.validate("ThisIsAVeryLongPassword123!")
        assert not is_valid
        assert any("ne doit pas dépasser 20" in error for error in errors)

    def test_password_exact_min_length(self, validator):
        is_valid, errors = validator.validate("Pass1234")
        assert is_valid or "spécial" in str(errors)

    def test_exactly_8_characters(self, validator):
        is_valid, errors = validator.validate("Pass1234")
        assert is_valid

    def test_exactly_20_characters(self, validator):
        is_valid, errors = validator.validate("Pass1234Pass1234Pass")
        assert is_valid

    def test_21_characters(self, validator):
        is_valid, errors = validator.validate("Pass1234Pass1234Pass!!")
        assert not is_valid


class TestPasswordSpaces:
    def test_password_with_spaces(self, validator):
        is_valid, errors = validator.validate("Pass 1234!")
        assert not is_valid
        assert any("espaces" in error for error in errors)

    def test_password_no_spaces(self, validator):
        is_valid, errors = validator.validate("Pass1234!")
        assert is_valid


class TestPasswordConsecutiveChars:
    def test_password_with_4_consecutive_identical(self, validator):
        is_valid, errors = validator.validate("Paaaass1!")
        assert not is_valid
        assert any("consécutifs" in error for error in errors)

    def test_password_with_3_consecutive_identical(self, validator):
        is_valid, errors = validator.validate("Paaa1234!")
        assert is_valid

    def test_password_with_no_consecutive_identical(self, validator):
        is_valid, errors = validator.validate("Pass1234!")
        assert is_valid


class TestPasswordCharacteristics:
    def test_password_with_all_4_characteristics(self, validator):
        is_valid, errors = validator.validate("Pass1234!")
        assert is_valid

    def test_password_with_3_characteristics_uppercase_lowercase_number(self, validator):
        is_valid, errors = validator.validate("Pass1234")
        assert is_valid

    def test_password_with_3_characteristics_uppercase_lowercase_special(self, validator):
        is_valid, errors = validator.validate("PassWord!")
        assert is_valid

    def test_password_with_only_2_characteristics(self, validator):
        is_valid, errors = validator.validate("PASSWORD")
        assert not is_valid
        assert any("3 des 4" in error for error in errors)

    def test_all_special_characters(self, validator):
        for special_char in "@#$%^&+=":
            password = f"Pass1234{special_char}"
            is_valid, _ = validator.validate(password)
            assert is_valid


class TestPasswordBlacklist:
    def test_common_password_rejected(self, validator):
        is_valid, errors = validator.validate("password123")
        assert not is_valid
        assert any("trop commun" in error for error in errors)

    def test_common_password_case_insensitive(self, validator):
        is_valid, errors = validator.validate("PASSWORD")
        assert not is_valid

    def test_unique_password_accepted(self, validator):
        is_valid, errors = validator.validate("MyUnique123!")
        assert is_valid


class TestPasswordStrength:
    def test_strength_weak(self, validator):
        strength = validator.get_strength("short")
        assert strength == PasswordStrength.WEAK

    def test_strength_medium(self, validator):
        strength = validator.get_strength("Pass1234")
        assert strength == PasswordStrength.MEDIUM

    def test_strength_strong(self, validator):
        strength = validator.get_strength("Pass1234!&")
        assert strength == PasswordStrength.STRONG


class TestPasswordIntegration:
    def test_valid_password_all_criteria(self, validator):
        password = "SecurePass123!"
        is_valid, errors = validator.validate(password)
        assert is_valid
        assert len(errors) == 0

    def test_validation_report(self, validator):
        password = "SecurePass123!"
        report = validator.get_validation_report(password)
        assert report["valid"] is True
        assert report["strength"] == "strong"
        assert report["characteristics"] == 4
        assert len(report["errors"]) == 0

    def test_validation_report_invalid(self, validator):
        password = "weak"
        report = validator.get_validation_report(password)
        assert report["valid"] is False
        assert len(report["errors"]) > 0
