# Password Validator 🔐

Un validateur de mots de passe asynchrone en Python avec architecture hexagonale et tests complets.

## 📋 Vue d'ensemble

Ce projet implémente un validateur de mots de passe robuste avec :
- **Architecture hexagonale** : Séparation clair entre domaine et infrastructure
- **Programmation asynchrone** : Méthodes async/await pour les opérations à long terme
- **Port/Adapter pattern** : Intégration flexible des services externes (vérification des fuites)
- **Configuration flexible** : Personnalisable via dataclasses
- **Suite de tests complète** : 25 tests avec pattern Arrange-Act-Assert

## 🎯 Fonctionnalités principales

- ✅ Validation stricte avec règles bloquantes et caractéristiques optionnelles
- ✅ Vérification asynchrone des mots de passe compromis (Breach Checker)
- ✅ Dégradation gracieuse en cas d'indisponibilité du service de breach
- ✅ Configuration entièrement personnalisable
- ✅ Évaluation de la force (invalid/weak/medium/strong)
- ✅ Messages d'erreur détaillés en français
- ✅ Type hints complets et mypy-compatible
- ✅ Tests unitaires avec pattern AAA (Arrange-Act-Assert)

## 📁 Structure du projet

```
Passwordvalidator/
├── src/
│   ├── passwordValidator.py      # Classe publique PasswordValidator (API simple)
│   ├── validation_service.py     # Service de validation (logique métier)
│   ├── breach_checker.py         # Port & adaptateurs (pattern hexagonal)
│   ├── types.py                  # Enums, dataclasses, types
│   └── rules.py                  # Règles de validation individuelles
├── tests/
│   └── test_passwordValidator.py # 25 tests avec pattern AAA
├── README.md
└── Passwordvalidator.iml
```

## 📖 Règles de validation

### Règles strictes (bloquantes)

Un mot de passe **doit respecter** toutes ces règles pour être considéré comme valide :

1. **Longueur** : 8 à 20 caractères (configurable)
   ```
   ❌ "Short1!" → Trop court
   ✅ "Pass1234!" → OK
   ❌ "VeryLongPassword1234567890!" → Trop long
   ```

2. **Pas d'espaces**
   ```
   ❌ "Pass word123!" → Contient espace
   ✅ "Password123!" → OK
   ```

3. **Caractères consécutifs** : Max 3 caractères identiques consécutifs
   ```
   ❌ "Paaaass1!" → 4 'a' consécutifs
   ✅ "Paaa1234!" → 3 'a' max
   ```

4. **Pas dans la liste noire** : Évite les mots de passe courants
   ```
   ❌ "password" → Mot de passe commun
   ✅ "SecurePass123!" → Unique
   ```

5. **Vérification des fuites** (optionnel avec BreachChecker)
   ```
   ❌ "breached123" → Trouvé dans une fuite connue
   ✅ "SecurePass123!" → Non compromis
   ```

### Règles de caractéristiques (tolérance : 1 manquant sur 4)

Le mot de passe doit contenir **au moins 3 sur 4** des éléments suivants :

- ✓ Au moins une **majuscule** (A-Z)
- ✓ Au moins une **minuscule** (a-z)
- ✓ Au moins un **chiffre** (0-9)
- ✓ Au moins un **caractère spécial** (!@#$%^&*()_+-=[]{}...) 

**Exemples** :
```
✅ "SecurePass123!"  → Toutes les 4 caractéristiques → STRONG
✅ "Pass1234"       → 3 caractéristiques (pas spécial) → MEDIUM
✅ "PassWord!"      → 3 caractéristiques (pas chiffre) → MEDIUM
❌ "PASSWORD1"      → 2 caractéristiques (pas minuscule/spécial) → INVALID
```

## 🚀 Installation et utilisation

### Installation

```bash
# Prérequis
python -m pip install pytest pytest-asyncio

# Cloner/télécharger le projet
cd passwordvalidator
```

### Utilisation basique

```python
import asyncio
from src.passwordValidator import PasswordValidator

async def main():
    validator = PasswordValidator()
    
    # Validation simple
    is_valid = await validator.validate("SecurePass123!")
    print(is_valid)  # True
    
    # Évaluation de la force
    strength = await validator.get_strength("Pass1234")
    print(strength)  # "medium"
    
    # Rapport complet
    report = await validator.get_validation_report("weak")
    print(report)
    # {
    #     "is_valid": False,
    #     "valid": False,
    #     "strength": "invalid",
    #     "errors": ["Le mot de passe doit contenir au moins 8 caractères."]
    # }

asyncio.run(main())
```

### Configuration personnalisée

```python
from src.passwordValidator import PasswordValidator
from src.types import ValidationConfig

# Configuration sur mesure
config = ValidationConfig(
    min_length=10,
    max_length=30,
    max_consecutive=2,
    characteristic_tolerance=0,  # Toutes les 4 caractéristiques requises
    common_passwords=["motdepasse", "admin123"]
)

validator = PasswordValidator(config)
report = await validator.get_validation_report("MyPassword123!")
```

### Avec vérification des fuites (Pattern Hexagonal)

```python
from src.passwordValidator import PasswordValidator
from src.breach_checker import FakeBreachChecker, SpyBreachChecker

# Test avec un fake (sans appel API)
fake_checker = FakeBreachChecker(["breached123", "exposed456"])
validator = PasswordValidator(breach_checker=fake_checker)

# Spy pour vérifier l'appel
spy_checker = SpyBreachChecker()
validator = PasswordValidator(breach_checker=spy_checker)
await validator.validate("SecurePass123!")
print(spy_checker.call_count)  # 1

# Production avec vérification réelle (pseudo-code)
# http_checker = HttpBreachChecker(api_url="https://api.pwnedpasswords.com")
# validator = PasswordValidator(breach_checker=http_checker)

report = await validator.get_validation_report("SecurePass123!")
print(report["errors"])  # [] si mot de passe safe
```

## 🧪 Tests

Les tests suivent le pattern **Arrange-Act-Assert** pour une clarté maximale.

### Lancer tous les tests

```bash
python -m pytest tests/test_passwordValidator.py -v
python -m pytest tests/test_passwordValidator.py --tb=short
```

### Lancer par catégorie

```bash
# Tests de longueur
python -m pytest -k TestPasswordLength -v

# Tests de force
python -m pytest -k TestPasswordStrength -v

# Tests du breach checker
python -m pytest -k TestBreachChecker -v

# Tests d'espace
python -m pytest -k TestPasswordSpaces -v

# Tests de caractères consécutifs
python -m pytest -k TestPasswordConsecutiveChars -v
```

### Exemple de test avec pattern AAA

```python
@pytest.mark.asyncio
async def test_strength_strong(self, validator):
    # Arrange
    password = "Pass1234!&"
    
    # Act
    report = await validator.get_validation_report(password)
    
    # Assert
    assert report["strength"] == "strong"
```

## 🏗️ Architecture hexagonale

### Diagramme

```
┌─────────────────────────────────────────┐
│   PasswordValidator (API Publique)      │  ← Adapter sortant
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│  PasswordValidationService (Domaine)    │
│  - Exécute les 9 règles de validation   │
│  - Coordonne le breach checker          │
│  - Calcule la force du mot de passe     │
└──────────────┬──────────────────────────┘
               │
    ┌──────────▼──────────────────┐
    │  BreachChecker (PORT)       │  ← Interface abstraite
    │  interface async             │
    └──┬──────────┬────────┬───────┘
       │          │        │
    ┌──▼──┐  ┌───▼──┐  ┌──▼──────┐
    │Fake │  │Failing│ │Spy      │  ← Adapters
    └─────┘  └───────┘ └─────────┘     (pour tests)
```

### Concepts clés

- **Domaine** : `PasswordValidationService` - aucune dépendance externe
- **Port** : `BreachChecker` - interface abstraite définissant le contrat
- **Adapters** : `FakeBreachChecker`, `FailingBreachChecker`, `SpyBreachChecker` - implémentations pour tests
- **Injection de dépendances** : Le breach_checker est optionnel et injectable

### Avantages

1. ✅ **Testable** : Injecter des fakes sans appeler d'API
2. ✅ **Flexible** : Changer d'implémentation sans modifier le domaine
3. ✅ **Dégradation gracieuse** : Si le breach check échoue, validation continue
4. ✅ **Maintenable** : Chaque responsabilité bien isolée

## 📊 Tableau de validation

| Mot de passe | Longueur | Caractères | Force | Breach | ✅/❌ |
|---|---|---|---|---|---|
| `SecurePass123!` | ✅ | 4/4 | strong | Safe | ✅ |
| `Pass1234` | ✅ | 3/4 | medium | Safe | ✅ |
| `PassWord!` | ✅ | 3/4 | medium | Safe | ✅ |
| `PASSWORD1` | ✅ | 2/4 | - | Safe | ❌ |
| `short` | ❌ Trop court | - | - | Safe | ❌ |
| `password` | ✅ | ✅ | - | Commun | ❌ |
| `Pass 123!` | ✅ | ✅ | ✅ | Espace | ❌ |
| `Paaaass1!` | ✅ | ✅ | ✅ | 4 'a' | ❌ |

## 🔑 Concepts importants

### Règles strictes vs Caractéristiques

```python
# STRICT : 1 échec = invalide
✅ Longueur (8-20 caractères)
✅ Pas d'espaces
✅ Max 3 caractères consécutifs
✅ Pas dans la liste noire
✅ Pas compromis (si vérification activée)

# CARACTÉRISTIQUES : tolérance de 1 (3/4 requis)
✓ Majuscule
✓ Minuscule
✓ Chiffre
✓ Caractère spécial
```

### Programmation asynchrone

Toutes les méthodes sont `async` pour permettre :
- Appels API non-bloquants (vérification des fuites)
- Intégration future avec des services externes
- Dégradation gracieuse en cas de timeout

```python
# ⚠️ Important : utiliser async/await !
is_valid = await validator.validate("password")  # ✅
is_valid = validator.validate("password")         # ❌ TypeError
```

## 🧬 Technologies

- **Python 3.13+** : Type hints modernes, syntaxe async/await
- **pytest 9.0+** : Framework de test léger et puissant
- **pytest-asyncio 1.3+** : Support natif des tests asynchrones
- **Dataclasses** : Configuration type-safe et immutable
- **ABC (Abstract Base Classes)** : Interfaces abstraites

## 📈 Statistiques du projet

- **25 tests** organisés en 7 catégories
- **Pattern AAA** (Arrange-Act-Assert) pour chaque test
- **9 règles** de validation indépendantes
- **100% de réussite** des tests
- **3 adaptateurs** pour le breach checker (Fake, Failing, Spy)
- **Architecture hexagonale** complète

## 🚦 Pattern de test - Arrange-Act-Assert

Chaque test suit cette structure :

```python
@pytest.mark.asyncio
async def test_example(self, validator):
    # ARRANGE : Préparer les données de test
    password = "TestPassword123!"
    expected_strength = "strong"
    
    # ACT : Exécuter le code à tester
    report = await validator.get_validation_report(password)
    
    # ASSERT : Vérifier les résultats
    assert report["strength"] == expected_strength
    assert report["is_valid"] is True
```

---

**Projet démontrant les patterns modernes de Python**
- **Fait avec** : Python 3.13 | pytest 9.0.3 | pytest-asyncio 1.3.0
- **Architecture** : Hexagonale (Ports & Adapters)
- **Tests** : 25 tests avec pattern AAA
- **État** : 100% de réussite ✅

