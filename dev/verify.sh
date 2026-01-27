#!/bin/bash
set -e

./install.sh

(cd ../backend && poetry run pyright)
(cd ../client && npm run type-check)
