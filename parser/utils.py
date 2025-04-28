class ListNested : 

    def __init__(self):
        self._setup()

    def _setup(self):
        self.current = ""
        self.tokens = []

    def tokenize(self, list_in_string:str):
        self.tokens = [] 
        self.current = ""
        for ch in list_in_string:
            if ch == "[":
                self._add_literal()
                self.tokens.append(["StartList"])
            elif ch == "]":
                self._add_literal()
                self.tokens.append(["EndList"])
            elif ch == ",":
                self._add_literal()
            elif ch.isdigit():
                self.current += ch
            elif ch.isspace():
                 self._add_literal()
            else:
                 self._add_literal()
                 raise ValueError(f"Unexpected character in list string: {ch}")
        self._add_literal()
        return self.tokens

    def _add_literal(self):
        if self.current:
            self.tokens.append(["Lit", self.current])
            self.current = ""

    def process_nested_liest(self, list_in_string:str):
         return self.tokenize(list_in_string)

class ParserList:
    def __init__(self):
        self.tok = ListNested()

    def parse(self, exp:str):
        tokens = self.tok.tokenize(exp)
        tokens = [t for t in tokens if t != ['Lit', '']]
        token_iter = iter(tokens)
        try:
            first_token = next(token_iter)
            if first_token != ["StartList"]:
                 raise ValueError("Expression must start with '['")
            result = self._parse_list(token_iter)
            try:
                 next(token_iter)
                 raise ValueError("Unexpected tokens after main list closes")
            except StopIteration:
                 pass
            return result
        except StopIteration:
            raise ValueError("Unexpected end of expression or malformed list")
        except ValueError as e:
             print(f"Parsing error: {e}")
             raise 

    def _parse_list(self, token_iter):
        """Parses the content of a list until 'EndList' is encountered."""
        lst = []
        while True:
            try:
                token = next(token_iter)
            except StopIteration:
                raise ValueError("Malformed list: Unexpected end of input while parsing list")

            if token == ["EndList"]:
                return lst
            elif token == ["StartList"]:
                nested_list = self._parse_list(token_iter)
                lst.append(nested_list)
            elif token[0] == "Lit":
                try:
                    num = int(token[1])
                    lst.append(num)
                except ValueError:
                    raise ValueError(f"Invalid number literal: {token[1]}")

            else:
                raise ValueError(f"Unexpected token during list parsing: {token}")



    











        
                

        
