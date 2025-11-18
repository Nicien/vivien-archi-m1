#!/bin/bash
set -e

./install.sh

(cd ../backend-vivien && poetry run pyright)
(cd ../client && npm run type-check)
