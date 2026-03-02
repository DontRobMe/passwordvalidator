import pytest
from src.passwordValidator import PasswordValidator


@pytest.fixture
def validator():
    return PasswordValidator()


class TestPasswordLength:
    def test_password_too_short(self, validator):
        report = validator.get_validation_report("Short1!")
        assert not report["is_valid"]
        assert any("8 caractères" in e for e in report["errors"])

    def test_password_too_long(self, validator):
        report = validator.get_validation_report("ThisIsAVeryLongPassword123!")
        assert not report["is_valid"]
        assert any("20 caractères" in e for e in report["errors"])

    def test_password_exact_min_length(self, validator):
        report = validator.get_validation_report("Pass1234")
        assert report["is_valid"]

    def test_exactly_8_characters(self, validator):
        report = validator.get_validation_report("Pass1234")
        assert report["is_valid"]

    def test_exactly_20_characters(self, validator):
        report = validator.get_validation_report("Pass1234Pass1234Pass")
        assert report["is_valid"]

    def test_21_characters(self, validator):
        report = validator.get_validation_report("Pass1234Pass1234Pass!!")
        assert not report["is_valid"]
        assert any("20 caractères" in e for e in report["errors"])


class TestPasswordSpaces:
    def test_password_with_spaces(self, validator):
        report = validator.get_validation_report("Pass 1234!")
        assert not report["is_valid"]
        assert any("espaces" in e for e in report["errors"])

    def test_password_no_spaces(self, validator):
        report = validator.get_validation_report("Pass1234!")
        assert report["is_valid"]


class TestPasswordConsecutiveChars:
    def test_password_with_4_consecutive_identical(self, validator):
        report = validator.get_validation_report("Paaaass1!")
        assert not report["is_valid"]
        assert any("consécutifs" in e for e in report["errors"])

    def test_password_with_3_consecutive_identical(self, validator):
        report = validator.get_validation_report("Paaa1234!")
        assert report["is_valid"]

    def test_password_with_no_consecutive_identical(self, validator):
        report = validator.get_validation_report("Pass1234!")
        assert report["is_valid"]


class TestPasswordCharacteristics:
    def test_password_with_all_4_characteristics(self, validator):
        report = validator.get_validation_report("Pass1234!")
        assert report["is_valid"]

    def test_password_with_3_characteristics_uppercase_lowercase_number(self, validator):
        report = validator.get_validation_report("Pass1234")
        assert report["is_valid"]

    def test_password_with_3_characteristics_uppercase_lowercase_special(self, validator):
        report = validator.get_validation_report("PassWord!")
        assert report["is_valid"]

    def test_password_with_only_2_characteristics(self, validator):
        report = validator.get_validation_report("PASSWORD1")
        assert not report["is_valid"]
        assert len(report["errors"]) > 0
        assert (
            any("minuscule" in e for e in report["errors"]) or
            any("chiffre" in e for e in report["errors"]) or
            any("caractère spécial" in e for e in report["errors"])
        )


class TestPasswordStrength:
    def test_strength_weak(self, validator):
        report = validator.get_validation_report("short")
        assert report["strength"] in ("weak", "invalid")

    def test_strength_medium(self, validator):
        report = validator.get_validation_report("Pass1234")
        assert report["strength"] == "medium"

    def test_strength_strong(self, validator):
        report = validator.get_validation_report("Pass1234!&")
        assert report["strength"] == "strong"


class TestPasswordIntegration:
    def test_valid_password_all_criteria(self, validator):
        password = "SecurePass123!"
        report = validator.get_validation_report(password)
        assert report["is_valid"]
        assert len(report["errors"]) == 0

    def test_validation_report(self, validator):
        password = "SecurePass123!"
        report = validator.get_validation_report(password)
        assert report["valid"] is True or report["is_valid"] is True
        assert report["strength"] == "strong"
        assert len(report["errors"]) == 0

    def test_validation_report_invalid(self, validator):
        password = "weak"
        report = validator.get_validation_report(password)
        assert report["valid"] is False or report["is_valid"] is False
        assert len(report["errors"]) > 0
