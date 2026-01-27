#!/bin/bash
set -e

# install
(cd ../backend && poetry install)
(cd ../client && npm install)

# generate openapi & typescript stubs
(cd ../backend && (PYTHONPATH=".." poetry run python generate_openapi.py))

# generate ../client/src/api/backend-schema.d.ts
(cd ../client && npm run generate)
