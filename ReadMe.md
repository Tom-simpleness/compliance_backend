# Compliance Backend

Système de back-end pour la conformité d'une entreprise de services financiers réglementée.

## Prérequis

- Python 3.9+
- pip
- virtualenv

## Installation rapide

```bash
git clone [URL_DU_REPO]
cd compliance_backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
```

## Exécuter les tests

```bash
pytest
```

## Structure du projet

```
src/
├── domain/         # Entités, objets-valeurs, agrégats
├── application/    # Services d'application
└── infrastructure/ # Implémentations concrètes (repositories)

tests/              # Tests unitaires
```
