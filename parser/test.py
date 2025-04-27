from .tokenizer import  Tokenizer
from .parser import Parser
from software_design.matching import Null, Lit, Either, Any


def test_tok_empty_string():
    assert Tokenizer().tok("") == []


def test_tok_any_either():
    assert Tokenizer().tok("*{abc,def}") == [
        ["Any"],
        ["EitherStart"],
        ["Lit", "abc"],
        ["Lit", "def"],
        ["EitherEnd"],
    ]


def test_parse_either_two_lit():
    assert Parser().parse("{abc,def}") == Either(
        [Lit("abc"), Lit("def")]
    )

def test_escape_characters():
    assert Tokenizer().tok("a\\*b\\{c\\,d\\}e\\\\f") == [
        ["Lit", "a*b{c,d}e\\f"]
    ]

def test_list_characteres():
    assert Tokenizer().tok("a[efc]m") == [
        ["Lit", "a"],
        ["EitherStart"],
        ["Lit", "efc"],
        ["EitherEnd"],
        ["Lit", "m"]
    ]

def test_list_characteres():
    assert Tokenizer().tok("a[!efc]m") == [
        ["Lit", "a"],
        ["Not","efc"],
        ["Lit", "m"]
    ]