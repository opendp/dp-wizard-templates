#!/bin/bash

set -euo pipefail

PDOC_ALLOW_EXEC=1 pdoc -o docs/ dp_wizard_templates
cp -a examples docs/

echo "Read docs at: docs/index.html"