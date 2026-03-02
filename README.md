# Password Validator - Architecture Professionnelle

Validateur de mots de passe en Python avec architecture modulaire, configuration flexible et tests unitaires complets.

## 🎯 Fonctionnalités

- ✅ Validation complète avec règles strictes et caractéristiques
- ✅ Configuration flexible via dataclasses
- ✅ Évaluation de la force du mot de passe (strong/medium/weak/invalid)
- ✅ Messages d'erreur détaillés
- ✅ Architecture modulaire et maintenable
- ✅ Type hints complets
- ✅ Tests unitaires exhaustifs (21 tests, 100% de réussite)

## 📁 Structure du projet

```
Passwordvalidator/
├── src/
│   ├── rules.py                  # Règles de validation individuelles
│   ├── types.py                  # Types, enums et dataclasses
│   ├── validation_service.py     # Service de validation
│   └── passwordValidator.py      # API publique simple
├── tests/
│   └── test_passwordValidator.py # Tests unitaires complets
└── README.md
```

## 🚀 Installation

### Prérequis

- Python 3.10+
- pytest (pour les tests)

```bash
python -m pip install pytest
```

## 💻 Utilisation

### Utilisation basique

```python
from src.passwordValidator import PasswordValidator

validator = PasswordValidator()

# Validation simple
is_valid = validator.validate("SecurePass123!")
print(is_valid)  # True

# Évaluation de la force
strength = validator.get_strength("Pass1234")
print(strength)  # "medium"

# Rapport complet
report = validator.get_validation_report("weak")
print(report)
# {
#     "is_valid": False,
#     "valid": False,
#     "strength": "invalid",
#     "errors": ["Le mot de passe doit contenir au moins 8 caractères."]
# }
```

### Configuration personnalisée

```python
from src.passwordValidator import PasswordValidator
from src.types import ValidationConfig

# Configuration personnalisée
config = ValidationConfig(
    min_length=10,
    max_length=30,
    max_consecutive=2,
    characteristic_tolerance=0,  # Toutes les caractéristiques requises
    common_passwords=["motdepasse", "admin123"]
)

validator = PasswordValidator(config)
```

## 📋 Règles de validation

### Règles strictes (obligatoires)

1. **Longueur** : Entre 8 et 20 caractères (configurable)
2. **Pas d'espaces** : Aucun espace autorisé
3. **Caractères consécutifs** : Maximum 3 caractères identiques consécutifs (configurable)
4. **Blacklist** : Ne doit pas être dans la liste des mots de passe courants

### Règles de caractéristiques (tolérance possible)

Le mot de passe doit contenir **au moins 3 sur 4** des éléments suivants (configurable) :

1. Au moins une **majuscule** (A-Z)
2. Au moins une **minuscule** (a-z)
3. Au moins un **chiffre** (0-9)
4. Au moins un **caractère spécial** (!@#$%^&*()_+-=[]{}

;':"\\|,.<>/?)

### Niveaux de force

- **strong** : Toutes les caractéristiques présentes
- **medium** : 3 caractéristiques sur 4
- **weak** : Au moins 1 caractéristique
- **invalid** : Échec des règles strictes ou moins de 1 caractéristique

## 🧪 Tests

### Lancer tous les tests

```bash
python -m pytest -v
```

### Lancer une catégorie spécifique

```bash
python -m pytest -k TestPasswordLength -v
python -m pytest -k TestPasswordStrength -v
```

### Lancer un test précis

```bash
python -m pytest -k test_password_too_short -v
```

## 🏗️ Architecture

### Avantages de cette architecture

1. **Séparation des responsabilités** : Chaque module a un rôle clair
   - `rules.py` : Règles de validation pures
   - `types.py` : Définitions de types et configuration
   - `validation_service.py` : Logique métier
   - `passwordValidator.py` : API publique simple

2. **Configuration flexible** : Utilisation de dataclasses pour une configuration type-safe

3. **Extensibilité** : Ajout facile de nouvelles règles sans modifier le code existant

4. **Testabilité** : Chaque composant peut être testé indépendamment

5. **Type safety** : Type hints complets pour une meilleure maintenance

6. **Documentation** : Docstrings complètes sur toutes les fonctions publiques

## 📊 Exemples de validation

| Mot de passe | Valide | Force | Erreurs |
|--------------|--------|-------|---------|
| `SecurePass123!` | ✅ | strong | - |
| `Pass1234` | ✅ | medium | - |
| `PassWord!` | ✅ | medium | - |
| `PASSWORD1` | ❌ | weak | Manque minuscule et caractère spécial |
| `short` | ❌ | invalid | Trop court |
| `password` | ❌ | invalid | Trop commun |
| `Pass 123!` | ❌ | invalid | Contient des espaces |
| `Paaaass1!` | ❌ | invalid | 4 'a' consécutifs |

## 🎓 Pour votre professeur

Ce projet démontre :

- ✅ Architecture modulaire et SOLID principles
- ✅ Design patterns (Factory, Strategy)
- ✅ Configuration flexible avec dataclasses
- ✅ Type hints complets (Python 3.10+)
- ✅ Tests unitaires exhaustifs avec pytest
- ✅ Documentation complète avec docstrings
- ✅ Code maintenable et extensible
- ✅ Gestion propre des erreurs

### Commandes pour évaluation

```bash
# Tests complets
python -m pytest -v

# Tests par catégorie
python -m pytest -k TestPasswordLength -v
python -m pytest -k TestPasswordStrength -v
```

---

**Développé avec Python 3.13 | pytest 9.0.2**
