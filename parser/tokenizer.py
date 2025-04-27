import string

CHARS = set(string.ascii_letters + string.digits)

class Tokenizer:
    def __init__(self):
        self._setup()

    def _setup(self):
        self.result = []
        self.sitwch_for_either = False
        self.is_it_not = False
        self.current = ""

    def tok(self, text):
        self._setup()
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == "\\" and i < len(text) - 1:
                self.current += text[i+1]
                i += 2 
                continue
            if ch == "*":
                self._add("Any")
            elif ch == "{":
                self._add("EitherStart")
            elif ch == ",":
                self._add(None)
            elif ch == "}":
                self._add("EitherEnd")
            elif ch == "[":
                if text[i+1] != "!":
                    self._add("EitherStart")
                    self.sitwch_for_either = True
                else : 
                    self._add(None)
                    self.is_it_not = True
                    i += 2 
                    continue
            elif ch == "]":
                if self.sitwch_for_either:    
                    self._add("EitherEnd")
                    self.sitwch_for_either = False
                else : 
                    self._add(None)
            elif ch in CHARS:
                self.current += ch
            else:
                raise NotImplementedError(f"what is '{ch}'?")
            i += 1
            
        self._add(None)
        print(self.result)
        return self.result
    
    def _add(self, thing):
        if len(self.current) > 0:
            if  self.is_it_not : 
                self.result.append(["Not", self.current])
                self.is_it_not = False
            else : 
                self.result.append(["Lit", self.current])
                
            self.current = ""
        if thing is not None:
            self.result.append([thing])

