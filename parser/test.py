from .tokenizer import  Tokenizer
from .parser import Parser
from software_design.matching import Null, Lit, Either, Any
from .utils import ListNested, ParserList


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


def test_netsed_list():
    assert ListNested().process_nested_liest("[43,[343,98],554]") == [
        ["StartList"],
        ["Lit", "43"],
        ["StartList"],
        ["Lit", "343"],
        ["Lit", "98"],
        ["EndList"],
        ["Lit", "554"],
        ["EndList"],
    ]

def test_nested_list_parser():
    assert ParserList().parse("[43,[343,98],554]") == [43,[343,98],554]

def test_nested_list_parser_():
    assert ParserList().parse("[[343,98],554]") == [[343, 98], 554]
