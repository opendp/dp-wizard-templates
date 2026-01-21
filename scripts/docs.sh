#!/bin/bash

set -euo pipefail

PDOC_ALLOW_EXEC=1 pdoc -o docs/ dp_wizard_templates
# Copying __pycache__ would cause problems:
mkdir docs/examples || true
cp examples/*.* docs/examples

echo "Docs available at: docs/index.html"