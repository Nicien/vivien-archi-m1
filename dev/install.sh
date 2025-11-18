#!/bin/bash
set -e

# install
(cd ../backend-vivien && poetry install)
(cd ../client && npm install)

# generate openapi & typescript stubs
(cd ../backend-vivien && poetry run python generate_openapi.py)

# generate ../client/src/api/backend-schema.d.ts
(cd ../client && npm run generate)
