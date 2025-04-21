class Lit:
    def __init__(self, chars, rest=None):
        self.chars = chars
        self.rest = rest

    def match(self, text, start=0):
        end = start + len(self.chars)
        if text[start:end] != self.chars:
            return False
        if self.rest:
            return self.rest.match(text, end)
        return end == len(text)
    

class Any:
    def __init__(self, rest=None):
        self.rest = rest

    def match(self, char, start=0):

        if self.rest is None:
            return True
        for i in range(start,len(char)):
            if self.rest.match(char,i):
                return True
        return False