from abc import ABC, abstractmethod
from typing import List
import hashlib
import aiohttp


class BreachChecker(ABC):
    @abstractmethod
    async def is_breached(self, password: str) -> bool:
        pass


class FakeBreachChecker(BreachChecker):
    def __init__(self, breached_passwords: List[str] = None):
        self.breached_passwords = breached_passwords or []

    async def is_breached(self, password: str) -> bool:
        return password in self.breached_passwords


class FailingBreachChecker(BreachChecker):
    async def is_breached(self, password: str) -> bool:
        raise Exception("Breach check failed")


class SpyBreachChecker(BreachChecker):
    def __init__(self):
        self.call_count = 0

    async def is_breached(self, password: str) -> bool:
        self.call_count += 1
        return False


class HttpBreachChecker(BreachChecker):
    """
    Vérification réelle des mots de passe compromis via l'API Have I Been Pwned
    Utilise k-anonymity : envoie seulement les 5 premiers caractères du SHA1 du mot de passe
    """

    def __init__(self, api_url: str = "https://api.pwnedpasswords.com/range/"):
        self.api_url = api_url

    async def is_breached(self, password: str) -> bool:
        """
        Vérifie si un mot de passe a été compromis sans l'envoyer en clair

        Pattern k-anonymity de Troy Hunt :
        1. Hasher le mot de passe en SHA1
        2. Envoyer les 5 premiers caractères à l'API
        3. Comparer le suffixe du hash avec les résultats
        """
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()

        prefix = sha1_hash[:5]
        suffix = sha1_hash[5:]

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.api_url}{prefix}", timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status != 200:
                        return False

                    text = await response.text()

                    for line in text.split('\r\n'):
                        if ':' in line:
                            response_suffix, _ = line.split(':')
                            if response_suffix == suffix:
                                return True

                    return False

        except Exception as e:
            print(f"Erreur during breach check: {e}")
            return False
