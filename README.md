# Password Validator

Ce projet fournit un validateur de mots de passe en Python, ainsi qu’une suite de tests unitaires avec `pytest`.

## 1. Règles de validation

Un mot de passe est **valide** s’il respecte toutes les règles suivantes :

1. Longueur :
   - Minimum **8** caractères
   - Maximum **20** caractères
2. Contenu :
   - Au moins **1 majuscule**
   - Au moins **1 minuscule**
   - Au moins **1 chiffre**
   - Au moins **1 caractère spécial** parmi : `@#$%^&+=`
3. Restrictions :
   - **Aucun espace**
   - **Pas plus de 3 caractères identiques consécutifs** (ex : `aaaa` est invalide)
   - **Ne doit pas faire partie** d’une liste de mots de passe courants (blacklist simple)
4. Complexité minimale :
   - Le mot de passe doit contenir **au moins 3 types** différents parmi :
     - majuscules
     - minuscules
     - chiffres
     - caractères spéciaux

Le validateur fournit aussi un **indice de force** du mot de passe :

- `weak` : faible
- `medium` : moyen
- `strong` : fort

## 2. Structure du projet

```text
C:\Users\Franc\IdeaProjects\Password validator
├─ src
│  └─ passwordValidator.py
└─ tests
   └─ test_passwordValidator.py
```

- `src/passwordValidator.py` : contient la classe `PasswordValidator` et l’énumération `PasswordStrength`.
- `tests/test_passwordValidator.py` : contient les tests unitaires organisés **par catégorie** (longueur, espaces, blacklist, force, etc.).

## 3. Prérequis

- Python 3.10+ recommandé
- `pip` installé
- `pytest` installé

### Installation de `pytest`

#### Sous Windows, Mac ou Linux (méthode universelle) :

```bash
python -m pip install pytest
```

#### Alternative (si `python` n'est pas reconnu, essayez `python3`) :

```bash
python3 -m pip install pytest
```

#### Ou, si `pip` est directement accessible :

```bash
pip install pytest
```

## 4. Utilisation du validateur dans votre code

Exemple minimal :

```python
from src.passwordValidator import PasswordValidator, PasswordStrength

validator = PasswordValidator()

password = "SecurePass123!"

is_valid, errors = validator.validate(password)
print("Valide :", is_valid)
print("Erreurs :", errors)

strength = validator.get_strength(password)
print("Force :", strength.value)

report = validator.get_validation_report(password)
print("Rapport :", report)
```

## 5. Lancer les tests

Placez-vous à la racine du projet :

### Sous Windows (PowerShell ou CMD) :

```powershell
cd "C:\Users\Franc\IdeaProjects\Passwordvalidator"
```

### Sous Mac/Linux (Terminal Bash) :

```bash
cd "~/IdeaProjects/Passwordvalidator"
```

### 5.1. Lancer **tous** les tests

#### Méthode universelle (fonctionne partout) :

```bash
python -m pytest -v
```

#### Si `pytest` est reconnu comme commande :

```bash
pytest -v
```

### 5.2. Lancer les tests **par catégorie (par classe)**

```bash
python -m pytest -k TestPasswordLength
python -m pytest -k TestPasswordStrength
python -m pytest -k TestPasswordIntegration
```

Ou, si `pytest` est reconnu :

```bash
pytest -k TestPasswordLength
```

### 5.3. Lancer un **seul test** précis

```bash
python -m pytest -k test_password_too_short
```

Ou :

```bash
pytest -k test_password_too_short
```

## 6. Dépannage

- **Erreur : `pytest` n'est pas reconnu**
  - Utilisez toujours `python -m pytest` au lieu de `pytest` seul.
  - Vérifiez que l'installation de pytest s'est bien passée :
    ```bash
    python -m pytest --version
    ```
  - Si vous avez plusieurs versions de Python, essayez `python3` à la place de `python`.

- **Problème d'import dans vos scripts**
  - Si vous obtenez une erreur d'import, vérifiez que vous exécutez votre script depuis la racine du projet ou que le dossier `src` est bien dans le PYTHONPATH.

## 7. Résumé rapide

- **Installer les dépendances** : `python -m pip install pytest`
- **Tous les tests** : `python -m pytest -v`
- **Par classe (catégorie)** : `python -m pytest -k TestPasswordLength`
- **Un seul test** : `python -m pytest -k test_strength_strong`

Le projet est conçu pour être simple à lancer et à étendre : ajoutez vos nouvelles règles dans `PasswordValidator` et vos nouveaux scénarios dans `tests/test_passwordValidator.py`.
