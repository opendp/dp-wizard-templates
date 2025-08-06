"""
DP Wizard Templates relies on code inspection, so real working examples
need to be in code. This file provides some motivation for the library,
and demonstrates how it can be used idiomatically.

## Motivation

Let's say you want to generate Python code programmatically,
perhaps to demonstrate a workflow with parameters supplied by the user.
One approach would be to use a templating system like Jinja,
but this may be hard to maintain: The template itself is not Python,
so syntax problems will not be obvious until it is filled in.
At the other extreme, constructing code via an AST is very low-level.

DP Wizard Templates is an alternative. The templates are themselves python code,
with the slots to fill in all-caps. This convention means that the template
itself can be parsed as python code, so syntax highlighting and linting still works.
"""

from dp_wizard_templates.code_template import Template


def conditional_print_template(CONDITION, MESSAGE):
    if CONDITION:
        print(MESSAGE)


conditional_print = (
    Template(conditional_print_template)
    .fill_expressions(CONDITION="temp_c < 0")
    .fill_values(MESSAGE="It is freezing!")
    .finish()
)

assert conditional_print == "if temp_c < 0:\nprint('It is freezing!')"

"""
Note the different methods used:
- `fill_expressions()` fills the slot with verbatim text.
  It can be used for an expression like this, or for variable names.
- `fill_values()` fills the slot with the repr of the provided value.
  This might be a string, or it might be a array or dict or other
  data structure, as long as it has a usable repr.
- `finish()` converts the template to a string, and will error
  if not all slots have been filled.

Templates can also be in standalone files. If a string is provided,
the system will prepend '_' and append '.py' and look for a corresponding file.
(The convention of prepending '_' reminds us that although these files
can be parsed, they should not be imported or executed as-is.)
"""

from pathlib import Path

block_demo = (
    Template("block_demo", root=Path(__file__).parent)
    .fill_expressions(FUNCTION_NAME="freeze_warning", PARAMS="temp_c")
    .fill_blocks(INNER_BLOCK=conditional_print)
    .finish()
)

assert (
    block_demo
    == '''def freeze_warning(temp_c):
    """
    This demonstrates how larger blocks of code can be built compositionally.
    """
    if temp_c < 0:
    print('It is freezing!')
'''
)
