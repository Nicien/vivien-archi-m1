# install.ps1
# Arrête le script si une erreur se produit
$ErrorActionPreference = "Stop"

# Installer les dépendances backend avec Poetry
Push-Location ..\backend
poetry install
Pop-Location

# Installer les dépendances frontend avec npm
Push-Location ..\client
npm install
Pop-Location

# Générer OpenAPI & TypeScript stubs
Push-Location ..\backend
poetry run python -m backend.generate_openapi
Pop-Location

# Générer ../client/src/api/backend-schema.d.ts
Push-Location ..\client
npm run generate
Pop-Location