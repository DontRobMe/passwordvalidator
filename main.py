import asyncio
from src.passwordValidator import PasswordValidator
from config import get_breach_checker

async def main():
    # Récupérer le breach checker approprié selon l'environnement
    breach_checker = get_breach_checker()

    # Créer le validateur avec le bon checker
    validator = PasswordValidator(breach_checker=breach_checker)

    test_passwords = [
        "SecurePass123!",
        "password",
        "Pass1234",
        "breached123",
        "weak",
    ]

    print("=" * 60)
    print("VALIDATEUR DE MOTS DE PASSE - Mode automatique")
    print("=" * 60)

    for password in test_passwords:
        report = await validator.get_validation_report(password)

        status = "✅ VALIDE" if report["is_valid"] else "❌ INVALIDE"
        strength = f"({report['strength'].upper()})" if report["is_valid"] else ""

        print(f"\n🔐 Mot de passe : '{password}' {status} {strength}")

        if report["errors"]:
            print("  ❌ Erreurs :")
            for error in report["errors"]:
                print(f"     - {error}")


if __name__ == "__main__":
    asyncio.run(main())

