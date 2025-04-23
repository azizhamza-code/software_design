from matching import Litt,PilotMachers, Anyy, Eitherr

def test_litt_matches_entire_string():
    # /abc/ matches "abc"
    assert Litt("abc")._match("abc")

def test_pilot_matchers_sequence_match():
    assert PilotMachers([Litt("abc"), Litt("bc")]).match("abcbc")

def test_pilot_matchers_with_any_fails_on_extra_chars():
    assert not PilotMachers([Litt("ab"), Anyy() , Litt("def")]).match("abGNdefLLL")

def test_pilot_matchers_with_any_succeeds():
    assert PilotMachers([Litt("ab"), Anyy() , Litt("def")]).match("abGNdef")

def test_pilot_matchers_with_any_at_end():
    assert PilotMachers([Litt("ab"), Anyy() , Litt("def"), Anyy()]).match("abGNdefLLL")

def test_pilot_matchers_any_litt_any():
    assert PilotMachers([ Anyy() , Litt("def"), Anyy()]).match("NdefLLL")

def test_pilot_matchers_any_litt_fails():
    assert not PilotMachers([ Anyy() , Litt("def")]).match("NdefLLL")

def test_pilot_matchers_any_litt_any_succeeds():
    assert PilotMachers([ Anyy() , Litt("def"), Anyy()]).match("NdefLLL")

def test_pilot_matchers_any_litt_any_or_succeeds():
    assert PilotMachers([ Anyy() , Litt("def"), Anyy(), Eitherr(Litt("LL"), Litt("PPP"))]).match("NdefLLL")

from matching import Litt, PilotMachers, Anyy, Eitherr

# Assuming your file is named matching.py
# If not, adjust the import statement above.

print("--- Testing Termination Conditions ---")

def test_pilot_matchers_fails_on_leftover_text():
    # Pattern matches prefix, but text has extra chars
    # Should fail because not all text is consumed.
    assert not PilotMachers([Litt("abc")]).match("abcd"), "Failed: Leftover text 'd'"

def test_pilot_matchers_fails_on_leftover_pattern():
    # Text matches prefix, but pattern has extra elements
    # Should fail because not all patterns are used.
    assert not PilotMachers([Litt("abc"), Litt("d")]).match("abc"), "Failed: Leftover pattern Litt('d')"

def test_pilot_matchers_empty_pattern_empty_text():
    # Empty pattern should match empty text
    assert PilotMachers([]).match(""), "Failed: Empty pattern on empty text"

def test_pilot_matchers_empty_pattern_non_empty_text():
    # Empty pattern should not match non-empty text
    assert not PilotMachers([]).match("a"), "Failed: Empty pattern on non-empty text"

def test_pilot_matchers_non_empty_pattern_empty_text():
    # Non-empty pattern should not match empty text
    assert not PilotMachers([Litt("a")]).match(""), "Failed: Non-empty pattern on empty text"

print("\n--- Testing Anyy Edge Cases ---")

def test_pilot_matchers_any_matches_zero_chars_at_start():
    # /*abc/ should match "abc"
    assert PilotMachers([Anyy(), Litt("abc")]).match("abc"), "Failed: Anyy matching zero at start"

def test_pilot_matchers_any_matches_zero_chars_at_end():
    # /abc*/ should match "abc"
    assert PilotMachers([Litt("abc"), Anyy()]).match("abc"), "Failed: Anyy matching zero at end"

def test_pilot_matchers_any_matches_zero_chars_in_middle():
    # /a*b/ should match "ab"
    assert PilotMachers([Litt("a"), Anyy(), Litt("b")]).match("ab"), "Failed: Anyy matching zero in middle"

def test_pilot_matchers_multiple_any_correct_match():
    # /a*b*c/ should match "axbyc"
    assert PilotMachers([Litt("a"), Anyy(), Litt("b"), Anyy(), Litt("c")]).match("axbyc"), "Failed: Multiple Anyy"

def test_pilot_matchers_multiple_any_match_zero():
    # /a*b*c/ should match "abc"
    assert PilotMachers([Litt("a"), Anyy(), Litt("b"), Anyy(), Litt("c")]).match("abc"), "Failed: Multiple Anyy matching zero"

print("\n--- Testing Eitherr Interaction ---")

def test_pilot_matchers_either_followed_by_literal_match_first():
    # /{a,b}c/ should match "ac"
    # This targets the core issue: does Eitherr correctly allow matching the 'rest'?
    assert PilotMachers([Eitherr(Litt("a"), Litt("b")), Litt("c")]).match("ac"), "Failed: Either(a,b)c on 'ac'"

def test_pilot_matchers_either_followed_by_literal_match_second():
    # /{a,b}c/ should match "bc"
    assert PilotMachers([Eitherr(Litt("a"), Litt("b")), Litt("c")]).match("bc"), "Failed: Either(a,b)c on 'bc'"

def test_pilot_matchers_either_followed_by_literal_no_match():
    # /{a,b}c/ should not match "ax"
    assert not PilotMachers([Eitherr(Litt("a"), Litt("b")), Litt("c")]).match("ax"), "Failed: Either(a,b)c no match 'ax'"

def test_pilot_matchers_literal_followed_by_either_match():
    # /a{b,c}/ should match "ab"
    assert PilotMachers([Litt("a"), Eitherr(Litt("b"), Litt("c"))]).match("ab"), "Failed: a + Either(b,c) on 'ab'"


print("\n--- Testing Complex Sequences & Indexing ---")

def test_pilot_matchers_complex_any_literal_match():
    # /a*bc*d/ should match "axyzbcqqd"
    assert PilotMachers([Litt("a"), Anyy(), Litt("bc"), Anyy(), Litt("d")]).match("axyzbcqqd"), "Failed: Complex Anyy/Lit sequence"

def test_pilot_matchers_complex_any_literal_fail():
    # /a*bc*d/ should not match "axyzbcd" (missing second Anyy match)
    assert not PilotMachers([Litt("a"), Anyy(), Litt("bc"), Anyy(), Litt("d")]).match("axyzbcd"), "Failed: Complex sequence expected fail"

