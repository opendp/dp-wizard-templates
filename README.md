# DP Wizard Templates

[![pypi](https://img.shields.io/pypi/v/dp_wizard_templates)](https://pypi.org/project/dp_wizard_templates/)

DP Wizard Templates lets you use syntactically valid Python code as a template.
Templates can be filled and composed to generate entire notebooks.

DP Wizard Templates was developed for [DP Wizard](https://github.com/opendp/dp-wizard),
and that codebase remains a good place to look for examples.


## Motivation

Let's say you want to generate Python code programmatically,
perhaps to demonstrate a workflow with parameters supplied by the user.
One approach would be to use a templating system like Jinja,
but this may be hard to maintain:
The template itself is not Python, so syntax problems will not be obvious until it is filled in.
At the other extreme, constructing code via an AST is very low-level.

## Usage

DP Wizard Templates is an alternative to template libraries and to AST.
The key is that the slots to fill are all-caps.
This convention means that the template itself can be treated as python code,
so IDE syntax highlighting and linters will still work.

Templates can be provided in a few different forms. First, as a string:

### Examples

### Hints


## Development

### Getting Started

On MacOS:
```shell
$ git clone https://github.com/opendp/dp-wizard-templates.git
$ cd dp-wizard-templates
$ brew install python@3.10
$ python3.10 -m venv .venv
$ source .venv/bin/activate
```

You can now install dependencies:
```shell
$ pip install -r requirements-dev.txt
$ pre-commit install
$ flit install
```

Tests should pass, and code coverage should be complete (except blocks we explicitly ignore):
```shell
$ scripts/ci.sh
```

### Release

- Make sure you're up to date, and have the git-ignored credentials file `.pypirc`.
- Make one last feature branch with the new version number in the name:
  - Run `scripts/changelog.py` to update the `CHANGELOG.md`.
  - Review the updates and pull a couple highlights to the top.
  - Bump `dp_wizard/VERSION`, and add the new number at the top of the `CHANGELOG.md`.
  - Commit your changes, make a PR, and merge this branch to main.
- Update `main` with the latest changes: `git checkout main; git pull`
- Publish: `flit publish --pypirc .pypirc`
