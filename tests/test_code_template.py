from dp_wizard_templates.code_template import (
    Token,
    _line_re,
    _slot_re,
    _Slots,
)


def test_line_re():
    assert _line_re.split("normal\n  indent\n  # comment") == [
        "",  # Always zero-length
        "",  # prefix
        "normal\n",
        "  ",  # prefix
        "indent\n",
        "  # ",  # prefix
        "comment",
    ]


def test_slot_re():
    assert _slot_re.split("A AB ABC ABC_XYZ TODO N0_NUMBERS") == [
        "A AB ",
        "ABC",  # slot
        " ",
        "ABC_XYZ",  # slot
        " ",
        "TODO",  # slot
        " N0_NUMBERS",
    ]


def test_slots_fill_inline():
    slots = _Slots("START and END")
    assert slots._tokens == [
        Token(string="", is_slot=False, is_prefix=True),
        Token(string="START", is_slot=True, is_prefix=False),
        Token(string=" and ", is_slot=False, is_prefix=False),
        Token(string="END", is_slot=True, is_prefix=False),
    ]
    slots.fill_inline("START", "END")
    slots.fill_inline("END", "START")
    assert slots.finish() == "END and START"


def test_slots_fill_block():
    slots = _Slots(
        """intro
CODE
    INDENTED
    # COMMENT"""
    )
    assert slots._tokens == [
        Token(string="", is_slot=False, is_prefix=True),
        Token(string="intro\n", is_slot=False, is_prefix=False),
        Token(string="", is_slot=False, is_prefix=True),
        Token(string="CODE", is_slot=True, is_prefix=False),
        Token(string="\n", is_slot=False, is_prefix=False),
        Token(string="    ", is_slot=False, is_prefix=True),
        Token(string="INDENTED", is_slot=True, is_prefix=False),
        Token(string="\n", is_slot=False, is_prefix=False),
        Token(string="    # ", is_slot=False, is_prefix=True),
        Token(string="COMMENT", is_slot=True, is_prefix=False),
    ]
    slots.fill_block("CODE", "if 'hello world':")
    slots.fill_block("INDENTED", "if foo:\n    bar()")
    slots.fill_block("COMMENT", "multi\nline")
    assert (
        slots.finish()
        == """intro
if 'hello world':
    if foo:
        bar()
    # multi
    # line"""
    )
