import json
import re
from pathlib import Path

import pytest

from dp_wizard_templates.converters import (
    ConversionException,
    _clean_nb,
    convert_nb_to_html,
    convert_nb_to_md,
    convert_py_to_nb,
)

fixtures_path = Path(__file__).parent / "fixtures"


def norm_nb(nb_str):
    nb_str = re.sub(r'"id": "[^"]+"', '"id": "12345678"', nb_str)
    nb_str = re.sub(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z",
        "2024-01-01T00:00:00.000000Z",
        nb_str,
    )

    nb = json.loads(nb_str)
    nb["metadata"] = {k: v for k, v in nb["metadata"].items() if k == "title"}
    for cell in nb["cells"]:
        metadata = cell["metadata"]
        if "execution" in metadata:
            metadata.pop("execution")

    return json.dumps(nb, indent=1)


def test_convert_py_to_nb():
    python_str = (fixtures_path / "fake.py").read_text()
    actual_nb_str = convert_py_to_nb(python_str, "Title!")
    (fixtures_path / "actual-fake.ipynb").write_text(actual_nb_str)
    expected_nb_str = (fixtures_path / "expected-fake.ipynb").read_text()

    normed_actual_nb_str = norm_nb(actual_nb_str)
    normed_expected_nb_str = norm_nb(expected_nb_str)
    assert normed_actual_nb_str == normed_expected_nb_str


def test_convert_py_to_nb_execute():
    python_str = (fixtures_path / "fake.py").read_text()
    actual_nb_str = convert_py_to_nb(python_str, "Title!", execute=True)
    (fixtures_path / "actual-fake-executed.ipynb").write_text(actual_nb_str)
    expected_nb_str = (fixtures_path / "expected-fake-executed.ipynb").read_text()

    normed_actual_nb_str = norm_nb(actual_nb_str)
    normed_expected_nb_str = norm_nb(expected_nb_str)
    assert normed_actual_nb_str == normed_expected_nb_str


def test_convert_nb_to_html():
    notebook = (fixtures_path / "expected-fake-executed.ipynb").read_text()
    actual_html = convert_nb_to_html(notebook)
    (fixtures_path / "actual-fake-executed.html").write_text(actual_html)
    assert "[1]:" in actual_html
    assert "<pre>4" in actual_html

    expected_html = (fixtures_path / "expected-fake-executed.html").read_text()
    assert actual_html == expected_html


def test_convert_nb_to_md():
    notebook = (fixtures_path / "expected-fake-executed.ipynb").read_text()
    actual_md = convert_nb_to_md(notebook)
    (fixtures_path / "actual-fake-executed.md").write_text(actual_md)
    assert "```python" in actual_md

    expected_md = (fixtures_path / "expected-fake-executed.md").read_text()
    assert actual_md == expected_md


def test_clean_nb():
    # Trivial test just to get 100% branch coverage.
    nb = {"cells": []}
    assert nb == json.loads(_clean_nb(json.dumps(nb)))


def test_convert_py_to_nb_error():
    python_str = "Invalid python!"
    with pytest.raises(
        ConversionException,
        # There's more, but what's most important is that
        # the line with the error shows up in the message.
        match=(r"Invalid python!"),
    ):
        convert_py_to_nb(python_str, "Title!", execute=True, reformat=False)
