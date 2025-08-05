from dp_wizard_templates.code_template import Template

# DP Wizard Templates is an alternative to template libraries and to AST.
# The key is that the slots to fill are all-caps.
# This convention means that the template itself can be treated as python code,
# so IDE syntax highlighting and linters will still work.

# Templates can be provided in a few different forms. The simplest option is a string:

template = Template("VAR = DOUBLE_ME * 2")
filled = template.fill_expressions(VAR="result").fill_values(DOUBLE_ME="Duran").finish()
assert filled == "result = 'Duran' * 2"

# Note the different fill methods:
# - `fill_expressions` will insert a string verbatim.
# - `fill_values` in contrast will insert a repr of your value.
#
# There is a third option, `fill_block`, which will be introduced shortly.
#
# The `finish` method, besides returning a string, will also check that all slots have been filled:

template = Template("LEFT = RIGHT")
try:
    template.fill_expressions(LEFT="my_variable").finish()
except Exception as e:
    assert "'RIGHT' slot not filled in string template" in str(e)


