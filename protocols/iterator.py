import pytest

class NaiveIterator:
    def __init__(self, text):
        self._text = text[:]

    def __iter__(self):
        self._row, self._col = 0, -1
        return self

    def __next__(self):
        self._advance()
        if self._row == len(self._text):
            raise StopIteration
        
        if len(self._text[self._row]) == 0: 
            raise StopIteration
        else : 
            return self._text[self._row][self._col]

    def _advance(self):
        if self._row < len(self._text):
            self._col += 1
            if self._col == len(self._text[self._row]):
                self._row += 1
                self._col = 0



class BetterIterator:
    def __init__(self, text):
        self._text = text[:]

    def __iter__(self):
        return BetterCursor(self._text)


class BetterCursor:
    def __init__(self, text):
        self._text = text
        self._row = 0
        self._col = -1

    def __next__(self):
        self._advance()
        if self._row == len(self._text):
            raise StopIteration
        return self._text[self._row][self._col]

    def _advance(self):
        if self._row < len(self._text):
            self._col += 1
            if self._col == len(self._text[self._row]):
                self._row += 1
                self._col = 0



def gather(buffer):
    result = ""
    for char in buffer:
        result += char
    return result


if __name__ =='__main__':


    def test_naive_buffer():
        buffer = NaiveIterator(["ab", "c"])
        assert gather(buffer) == "abc"

    def test_naive_buffer_empty_string():
        buffer = NaiveIterator(["a", ""])
        assert gather(buffer) == "a"

    test_naive_buffer_empty_string()

    def test_naive_buffer_nested_loop():
        buffer = BetterIterator(["a", "b"])
        result = ""
        for outer in buffer:
            for inner in buffer:
                result += inner
        assert result == "abab"

    test_naive_buffer_nested_loop()