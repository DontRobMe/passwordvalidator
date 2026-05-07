import pytest
from src.passwordValidator import PasswordValidator


@pytest.fixture
def validator():
    return PasswordValidator()


class TestPasswordLength:
    """Vérifie que les mots de passe doivent faire entre 8 et 20 caractères"""

    @pytest.mark.asyncio
    async def test_password_too_short(self, validator):
        """Un mot de passe avec seulement 7 caractères doit être rejeté"""
        # Arrange
        password = "Short1!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert not report["is_valid"]
        assert any("8 caractères" in e for e in report["errors"])

    @pytest.mark.asyncio
    async def test_password_too_long(self, validator):
        """Un mot de passe avec plus de 20 caractères doit être rejeté"""
        # Arrange
        password = "ThisIsAVeryLongPassword123!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert not report["is_valid"]
        assert any("20 caractères" in e for e in report["errors"])

    @pytest.mark.asyncio
    async def test_password_exact_min_length(self, validator):
        """Un mot de passe avec exactement 8 caractères (minimum) doit être accepté"""
        # Arrange
        password = "Pass1234"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_exactly_8_characters(self, validator):
        """Confirmer qu'un mot de passe de 8 caractères est valide"""
        # Arrange
        password = "Pass1234"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_exactly_20_characters(self, validator):
        """Un mot de passe avec exactement 20 caractères (maximum) doit être accepté"""
        # Arrange
        password = "Pass1234Pass1234Pass"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_21_characters(self, validator):
        """Un mot de passe avec 21 caractères dépasse la limite et doit être rejeté"""
        # Arrange
        password = "Pass1234Pass1234Pass!!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert not report["is_valid"]
        assert any("20 caractères" in e for e in report["errors"])


class TestPasswordSpaces:
    """Vérifie que les espaces ne sont pas autorisés dans les mots de passe"""

    @pytest.mark.asyncio
    async def test_password_with_spaces(self, validator):
        """Un mot de passe contenant un espace doit être rejeté"""
        # Arrange
        password = "Pass 1234!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert not report["is_valid"]
        assert any("espaces" in e for e in report["errors"])

    @pytest.mark.asyncio
    async def test_password_no_spaces(self, validator):
        """Un mot de passe sans espace doit être accepté (si les autres règles sont respectées)"""
        # Arrange
        password = "Pass1234!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]


class TestPasswordConsecutiveChars:
    """Vérifie qu'un mot de passe ne peut pas avoir plus de 3 caractères identiques consécutifs"""

    @pytest.mark.asyncio
    async def test_password_with_4_consecutive_identical(self, validator):
        """Un mot de passe avec 4 fois le même caractère d'affilée doit être rejeté"""
        # Arrange
        password = "Paaaass1!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert not report["is_valid"]
        assert any("consécutifs" in e for e in report["errors"])

    @pytest.mark.asyncio
    async def test_password_with_3_consecutive_identical(self, validator):
        """Un mot de passe avec maximum 3 caractères identiques d'affilée doit être accepté"""
        # Arrange
        password = "Paaa1234!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_password_with_no_consecutive_identical(self, validator):
        """Un mot de passe comme 'Pass1234!' sans caractères répétés doit être accepté"""
        # Arrange
        password = "Pass1234!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]


class TestPasswordCharacteristics:
    """Vérifie que les mots de passe doivent contenir au moins 3 types différents de caractères"""

    @pytest.mark.asyncio
    async def test_password_with_all_4_characteristics(self, validator):
        """Un mot de passe avec majuscules, minuscules, chiffres ET caractères spéciaux doit être accepté"""
        # Arrange
        password = "Pass1234!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_password_with_3_characteristics_uppercase_lowercase_number(self, validator):
        """Un mot de passe avec majuscules, minuscules et chiffres (sans caractère spécial) doit être accepté"""
        # Arrange
        password = "Pass1234"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_password_with_3_characteristics_uppercase_lowercase_special(self, validator):
        """Un mot de passe avec majuscules, minuscules et caractère spécial (sans chiffre) doit être accepté"""
        # Arrange
        password = "PassWord!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_password_with_only_2_characteristics(self, validator):
        """Un mot de passe avec seulement 2 types de caractères doit être rejeté"""
        # Arrange
        password = "PASSWORD1"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert not report["is_valid"]
        assert len(report["errors"]) > 0
        assert (
            any("minuscule" in e for e in report["errors"]) or
            any("chiffre" in e for e in report["errors"]) or
            any("caractère spécial" in e for e in report["errors"])
        )


class TestPasswordStrength:
    """Vérifie que le validateur calcule correctement la force d'un mot de passe"""

    @pytest.mark.asyncio
    async def test_strength_weak(self, validator):
        """Un mot de passe trop court doit avoir une force faible ou invalide"""
        # Arrange
        password = "short"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["strength"] in ("weak", "invalid")

    @pytest.mark.asyncio
    async def test_strength_medium(self, validator):
        """Un mot de passe avec 3 caractéristiques sur 4 doit avoir une force moyenne"""
        # Arrange
        password = "Pass1234"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["strength"] == "medium"

    @pytest.mark.asyncio
    async def test_strength_strong(self, validator):
        """Un mot de passe avec les 4 caractéristiques doit avoir une force forte"""
        # Arrange
        password = "Pass1234!&"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["strength"] == "strong"


class TestPasswordIntegration:
    """Teste le validateur dans un contexte réel avec tous les critères ensemble"""

    @pytest.mark.asyncio
    async def test_valid_password_all_criteria(self, validator):
        """Un mot de passe qui respecte TOUS les critères doit être valide sans erreurs"""
        # Arrange
        password = "SecurePass123!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]
        assert len(report["errors"]) == 0

    @pytest.mark.asyncio
    async def test_validation_report(self, validator):
        """Le rapport de validation doit donner les bonnes informations : validité, force et absence d'erreurs"""
        # Arrange
        password = "SecurePass123!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["valid"] is True or report["is_valid"] is True
        assert report["strength"] == "strong"
        assert len(report["errors"]) == 0

    @pytest.mark.asyncio
    async def test_validation_report_invalid(self, validator):
        """Un mot de passe invalide doit générer un rapport avec des erreurs"""
        # Arrange
        password = "weak"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["valid"] is False or report["is_valid"] is False
        assert len(report["errors"]) > 0


class TestBreachChecker:
    """Teste la vérification des mots de passe compromis (fuites de données)"""

    @pytest.fixture
    def fake_breached_checker(self):
        from src.breach_checker import FakeBreachChecker
        return FakeBreachChecker(["breached123"])

    @pytest.fixture
    def failing_breached_checker(self):
        from src.breach_checker import FailingBreachChecker
        return FailingBreachChecker()

    @pytest.fixture
    def spy_breached_checker(self):
        from src.breach_checker import SpyBreachChecker
        return SpyBreachChecker()

    @pytest.mark.asyncio
    async def test_password_not_breached(self, fake_breached_checker):
        """Un mot de passe qui n'est pas trouvé dans la liste des mots de passe compromis doit être accepté"""
        # Arrange
        validator = PasswordValidator(breach_checker=fake_breached_checker)
        password = "SecurePass123!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_password_breached(self, fake_breached_checker):
        """Un mot de passe trouvé dans la liste des compromis doit être rejeté"""
        # Arrange
        validator = PasswordValidator(breach_checker=fake_breached_checker)
        password = "breached123"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        assert not report["is_valid"]
        assert any("compromis" in e for e in report["errors"])

    @pytest.mark.asyncio
    async def test_breach_check_fails_gracefully(self, failing_breached_checker):
        """Si la vérification des fuites échoue (ex: API indisponible), on continue quand même"""
        # Arrange
        validator = PasswordValidator(breach_checker=failing_breached_checker)
        password = "SecurePass123!"
        # Act
        report = await validator.get_validation_report(password)
        # Assert
        # Should still be valid since breach check is skipped
        assert report["is_valid"]

    @pytest.mark.asyncio
    async def test_breach_checker_called_once(self, spy_breached_checker):
        """La vérification des fuites doit être appelée exactement une fois par validation"""
        # Arrange
        validator = PasswordValidator(breach_checker=spy_breached_checker)
        password = "SecurePass123!"
        # Act
        await validator.validate(password)
        # Assert
        assert spy_breached_checker.call_count == 1
