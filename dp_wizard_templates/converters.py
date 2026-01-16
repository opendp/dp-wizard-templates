import hashlib
import json
import re
import subprocess
import warnings
from dataclasses import dataclass
from pathlib import Path
from sys import executable
from tempfile import TemporaryDirectory

import black
import jupytext
import nbconvert
import nbformat
import nbformat.warnings


def _is_kernel_installed() -> bool:
    try:
        # This method isn't well documented, so it may be fragile.
        jupytext.kernels.kernelspec_from_language("python")  # type: ignore
        return True
    except ValueError:  # pragma: no cover
        return False


@dataclass(frozen=True)
class ConversionException(Exception):
    command: str
    stderr: str

    def __str__(self):
        return f"Script to notebook conversion failed: {self.command}\n{self.stderr})"


def _preprocess_one_line(target, following) -> str:
    if following.startswith("\n#") and not following.startswith("\n# %"):
        target += " [markdown]"
    return target


def _preprocess_all_blocks(python_str: str) -> str:
    splits = re.split(r"(^#\s+\+.*)", python_str, flags=re.MULTILINE)
    for i in range(len(splits)):
        if i % 2 == 1:
            splits[i] = _preprocess_one_line(splits[i], splits[i + 1])
    return "".join(splits)


def convert_to_notebook(
    python_str: str, title: str, execute: bool = False, reformat: bool = True
) -> dict:
    """
    Given Python code as a string, returns a notebook as a string of JSON.
    (Calls jupytext as a subprocess:
    Not ideal, but only the CLI is well documented.)
    """
    python_str = _preprocess_all_blocks(python_str)
    with TemporaryDirectory() as temp_dir:
        if not _is_kernel_installed():
            subprocess.run(  # pragma: no cover
                [executable]
                + "-m ipykernel install --name kernel_name --user".split(" "),
                check=True,
            )

        temp_dir_path = Path(temp_dir)
        py_path = temp_dir_path / "input.py"
        if reformat:
            # Line length determined by PDF rendering.
            python_str = black.format_str(python_str, mode=black.Mode(line_length=74))
        py_path.write_text(python_str)

        argv = [executable] + "-m jupytext --from .py --to .ipynb --output -".split(" ")
        if execute:
            argv.append("--execute")
        argv.append(str(py_path.absolute()))  # type: ignore
        result = subprocess.run(argv, text=True, capture_output=True)
    if result.returncode != 0:
        # If there is an error, we want a copy of the file that will stay around,
        # outside the "with TemporaryDirectory()" block.
        # The command we show in the error message isn't exactly what was run,
        # but it should reproduce the error.
        debug_path = Path("/tmp/script.py")
        debug_path.write_text(python_str)
        argv.pop()
        argv.append(str(debug_path))  # type: ignore
        raise ConversionException(command=" ".join(argv), stderr=result.stderr)
    nb_dict = json.loads(result.stdout.strip())
    nb_dict["metadata"]["title"] = title
    return _clean_nb(nb_dict)


def _stable_hash(lines: list[str]) -> str:
    return hashlib.sha1("\n".join(lines).encode()).hexdigest()[:8]


def _clean_nb(nb_dict: dict) -> dict:
    """
    Given a notebook as a string of JSON, remove pip output
    and make IDs stable.
    """
    new_cells = []
    for cell in nb_dict["cells"]:
        if "pip install" in cell["source"][0]:
            cell["outputs"] = []
        # Make ID stable:
        cell["id"] = _stable_hash(cell["source"])
        # Delete execution metadata:
        try:
            del cell["metadata"]["execution"]
        except KeyError:
            pass
        new_cells.append(cell)
    nb_dict["cells"] = new_cells
    return nb_dict


_default_exporter = nbconvert.HTMLExporter(
    template_name="lab",
    # The "classic" template's CSS forces large code cells on to
    # the next page rather than breaking, so use "lab" instead.
)


def convert_from_notebook(
    notebook_dict: dict,
    exporter: nbconvert.Exporter = _default_exporter,
) -> str:
    with warnings.catch_warnings():
        warnings.simplefilter(
            action="ignore", category=nbformat.warnings.DuplicateCellId
        )
        notebook_node = nbformat.reads(json.dumps(notebook_dict), as_version=4)
    (body, _resources) = exporter.from_notebook_node(notebook_node)
    # TODO: Pyright thinks body is a NotebookNode, but that's not right.
    return body  # pyright: ignore[reportReturnType]
