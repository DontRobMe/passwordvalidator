from src.validation_service import PasswordValidationService
from src.types import ValidationConfig


class PasswordValidator:

    def __init__(self, config: ValidationConfig = None):
        self.service = PasswordValidationService(config)

    def validate(self, password: str) -> bool:
        result = self.service.validate(password)
        return result.is_valid

    def get_strength(self, password: str) -> str:
        result = self.service.validate(password)
        return result.strength.value

    def get_validation_report(self, password: str) -> dict:
        result = self.service.validate(password)
        return result.to_dict()
