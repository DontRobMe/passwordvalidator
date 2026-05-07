from src.validation_service import PasswordValidationService
from src.types import ValidationConfig


class PasswordValidator:

    def __init__(self, config: ValidationConfig = None, breach_checker=None):
        self.service = PasswordValidationService(config, breach_checker)

    async def validate(self, password: str) -> bool:
        result = await self.service.validate(password)
        return result.is_valid

    async def get_strength(self, password: str) -> str:
        result = await self.service.validate(password)
        return result.strength.value

    async def get_validation_report(self, password: str) -> dict:
        result = await self.service.validate(password)
        return result.to_dict()
