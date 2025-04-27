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
        self._cash = {}

    def match(self, char, start=0):
        memo = {}
        key = id(self.rest.char)
        if self.rest is None:
            return True
        for i in range(start,len(char)):
            if self.rest.match(char,i):
                return True
        return False
    

class Either:
    def __init__(self, left, right, rest=None):
        self.left = left
        self.right = right
        self.rest = rest

    def match(self, text, start=0):
        return self.left.match(text, start) or \
            self.right.match(text, start)


class Match:
    def __init__(self, rest):
        self.rest = rest if rest is not None else Null()

    def __eq__(self, other):
        return (other is not None and
                self.__class__ == other.__class__ and
                self.rest == other.rest)

    def match(self, text):
        result = self._match(text, 0)
        return result ==len(text)
    
class Null(Match):
    def __init__(self):
        self.rest = None

    def _match(self, text, start):
        return start
    
class Plus(Match):
    def __init__(self, rest):
        super().__init__(rest)
    
    def _match(self, char, start):
        for i in range(start + 1 , len(char)+ 1):
            end = self.rest._match(char, i)
            if end == len (char):
                return end
        return None


class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def __eq__(self, other):
        return super().__eq__(other) and (
            self.chars == other.chars
        )

    def _match(self, text, start):
        end = start + len(self.chars)
        if text[start:end] != self.chars:
            return None
        return self.rest._match(text, end)
    
class Fromset(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def _match(self, text, start):
        if text[start] not in self.chars:
            return None
        return self.rest._match(text, start+1)
        


class Range(Match):
    Minuscules = "abcdefghijklmnopqrstuvwxyz"
    def __init__(self, start, end, rest = None):
        super().__init__(rest)
        self.start = start
        self.end = end

    def _match(self, text, start):
        if text[start] not in self.Minuscules[self.Minuscules.index(self.start): self.Minuscules.index(self.end)]:
            return None
        return self.rest._match(text, start+1)



class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)
        self._cache = {}

    def _match(self, char, start):
        for i in range(start, len(char)+ 1):
            end = self.rest._match(char, i)
            if end == len (char):
                return end
        return None
    

    

class Not(Match):
    def __init__(self, pattern:Match):
        super().__init__(None)
        self.pattern = pattern

    def _match(self, text, start):
        if self.pattern.match(text):
            return None
        return self.rest._match(text, len(text))
        
            

class Either(Match):
    def __init__(self, pattern:list,  rest=None):
        super().__init__(rest)
        self.pattern = pattern

    def _match(self, text, start):
        for pat in self.pattern:
            end = pat._match(text, start)
            if end is not None:
                end = self.rest._match(text, end)
                if end == len(text):
                    return end
        return None
    

from dataclasses import dataclass

@dataclass
class Anyy:
    type:str='any'

    def _match(self, text, start=0, switch_card=False):
        pass
@dataclass
class Litt:
    chars:str
    type:str='lit'
    def _match(self, text, start=0):
            if text[start:start + len(self.chars)]!= self.chars:
                return False , None
            else : 
                return True , None

@dataclass            
class Eitherr:
    right : Litt
    left : Litt
    type:str = 'eithier'

    def _match(self, text, start):
            if ( self.right._match(text, start) or self.left._match(text, start)):
                if self.right._match(text, start):
                    return True, self.right
                else:
                    return True, self.left
            return False
class PilotMachers:
    def __init__(self, matchers:list):
        self.list_of_matchers = matchers

    def match(self, text):
        indice = 0
        indice_matcher = 0
        while indice<len(text):
            matcher_finished_before_text = indice_matcher >= len(self.list_of_matchers)
            if matcher_finished_before_text:
                return False
            matcher = self.list_of_matchers[indice_matcher]
            if matcher.type != "any":
                result, left_right = matcher._match(text, indice)
                if result:
                    if left_right is not None:
                        indice = indice + len(left_right.chars) - 1
                    else :
                        indice = indice + len(matcher.chars) - 1
                else:
                    return False
            elif matcher.type == "any":
                with_break = False
                any_as_the_end = indice_matcher + 1 == len(self.list_of_matchers)
                if any_as_the_end:
                    return True
                next_matcher = self.list_of_matchers[indice_matcher + 1]
                while indice<len(text):
                    result,_ = next_matcher._match(text, indice+1)
                    if result :
                        with_break = True
                        break
                    indice = indice + 1
                if not with_break:
                    return False
            indice = indice + 1
            indice_matcher = indice_matcher + 1

        if indice ==len(text) and indice_matcher < len(self.list_of_matchers): 
            return False
                
        return True