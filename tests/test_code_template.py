import pytest
from dp_wizard_templates.code_template import Template


def test_def_too_long():
    def template(
        BEGIN,
        END,
    ):
        print(BEGIN, END)

    with pytest.raises(Exception, match=r"def and parameters should fit on one line"):
        Template(template)


def test_def_template():
    def template(BEGIN, END):
        print(BEGIN, END)

    assert (
        Template(template).fill_values(BEGIN="abc", END="xyz").finish()
        == "print('abc', 'xyz')"
    )


def test_fill_expressions():
    template = Template("No one VERB the ADJ NOUN!")
    filled = template.fill_expressions(
        VERB="expects",
        ADJ="Spanish",
        NOUN="Inquisition",
    ).finish()
    assert filled == "No one expects the Spanish Inquisition!"


def test_fill_expressions_missing_slots_in_template():
    template = Template("No one ... the ... ...!")
    with pytest.raises(
        Exception,
        match=r"no 'ADJ' slot to fill with 'Spanish', "
        r"no 'NOUN' slot to fill with 'Inquisition', "
        r"no 'VERB' slot to fill with 'expects':",
    ):
        template.fill_expressions(
            VERB="expects",
            ADJ="Spanish",
            NOUN="Inquisition",
        ).finish()


def test_fill_expressions_extra_slots_in_template():
    template = Template("No one VERB ARTICLE ADJ NOUN!")
    with pytest.raises(
        Exception, match=r"'ARTICLE' slot not filled, 'VERB' slot not filled"
    ):
        template.fill_expressions(
            ADJ="Spanish",
            NOUN="Inquisition",
        ).finish()


def test_fill_values():
    template = Template("assert [STRING] * NUM == LIST")
    filled = template.fill_values(
        STRING="🙂",
        NUM=3,
        LIST=["🙂", "🙂", "🙂"],
    ).finish()
    assert filled == "assert ['🙂'] * 3 == ['🙂', '🙂', '🙂']"


def test_fill_values_missing_slot_in_template():
    template = Template("assert [STRING] * ... == LIST")
    with pytest.raises(Exception, match=r"no 'NUM' slot to fill with '3'"):
        template.fill_values(
            STRING="🙂",
            NUM=3,
            LIST=["🙂", "🙂", "🙂"],
        ).finish()


def test_fill_values_extra_slot_in_template():
    template = Template("CMD [STRING] * NUM == LIST")
    with pytest.raises(Exception, match=r"'CMD' slot not filled"):
        template.fill_values(
            STRING="🙂",
            NUM=3,
            LIST=["🙂", "🙂", "🙂"],
        ).finish()


def test_fill_blocks():
    # "OK" is less than three characters, so it is not a slot.
    template = Template(
        """# MixedCase is OK

FIRST

with fake:
    my_tuple = (
        # SECOND
        VALUE,
    )
    if True:
        THIRD
""",
    )
    filled = (
        template.fill_code_blocks(
            FIRST="\n".join(f"import {i}" for i in "abc"),
            THIRD="\n".join(f"{i}()" for i in "xyz"),
        )
        .fill_comment_blocks(
            SECOND="This is a\nmulti-line comment",
        )
        .fill_values(VALUE=42)
        .finish()
    )
    assert (
        filled
        == """# MixedCase is OK

import a
import b
import c

with fake:
    my_tuple = (
        # This is a
        # multi-line comment
        42,
    )
    if True:
        x()
        y()
        z()
"""
    )


def test_fill_blocks_missing_slot_in_template_alone():
    template = Template("No block slot")
    with pytest.raises(Exception, match=r"no 'SLOT' slot to fill with 'placeholder':"):
        template.fill_code_blocks(SLOT="placeholder").finish()


def test_fill_blocks_missing_slot_in_template_not_alone():
    template = Template("No block SLOT")
    with pytest.raises(
        Exception,
        match=r"no 'SLOT' slot to fill with 'placeholder' "
        r"\(block slots must be alone on line\)",
    ):
        template.fill_code_blocks(SLOT="placeholder").finish()


def test_fill_blocks_extra_slot_in_template():
    template = Template("EXTRA\nSLOT")
    with pytest.raises(Exception, match=r"'EXTRA' slot not filled"):
        template.fill_code_blocks(SLOT="placeholder").finish()


def test_fill_blocks_not_string():
    template = Template("SOMETHING")
    with pytest.raises(
        Exception,
        match=r"for 'SOMETHING' slot, expected string, not '123'",
    ):
        template.fill_code_blocks(SOMETHING=123).finish()
