# DP Wizard Templates

[![pypi](https://img.shields.io/pypi/v/dp_wizard_templates)](https://pypi.org/project/dp_wizard_templates/)

DP Wizard Templates lets you use syntactically valid Python code as a template.
Templates can be filled and composed to generate entire notebooks.

See the [documentation](https://opendp.github.io/dp-wizard-templates) for more information.


## Development

### Getting Started

```shell
$ git clone https://github.com/opendp/dp-wizard-templates.git
$ cd dp-wizard-templates
$ pip install uv # if not already installed
$ uv sync
```

Tests should pass, and code coverage should be complete (except blocks we explicitly ignore):
```shell
$ uv run scripts/ci.sh
```

Docs can be previewed locally:
```shell
$ uv run scripts/docs.sh
```

### Release

- Make one last feature branch with the new version number in the name:
  - Run `uv run scripts/changelog.py` to update the `CHANGELOG.md`.
  - Review the updates and pull a couple highlights to the top.
  - `uv version --bump minor`, and add the new number at the top of the `CHANGELOG.md`.
  - Commit your changes, make a PR, and merge this branch to main.
- Update `main` with the latest changes: `git checkout main; git pull`
- With `~/.pypirc` in place, run `uvx uv-publish`.
