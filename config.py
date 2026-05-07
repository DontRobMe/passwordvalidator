"""
Configuration du validateur selon l'environnement
"""
import os
from src.breach_checker import FakeBreachChecker, HttpBreachChecker, BreachChecker

# Récupérer l'environnement depuis une variable d'env
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")


def get_breach_checker() -> BreachChecker:
    """
    Retourne le bon BreachChecker selon l'environnement

    - DEV : FakeBreachChecker (rapide, pas d'API)
    - PROD : HttpBreachChecker (vrai vérification Have I Been Pwned)
    """

    if ENVIRONMENT == "production":
        print("🔴 Mode PRODUCTION : vérification réelle des fuites activée")
        return HttpBreachChecker(api_url="https://api.pwnedpasswords.com/range/")

    else:
        print("🟢 Mode DÉVELOPPEMENT : fake checker (sans API)")
        # En dev, faux positifs : password compromis = "password", "123456", "breached"
        return FakeBreachChecker(["password", "123456", "breached123"])