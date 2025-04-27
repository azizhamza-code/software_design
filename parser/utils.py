class ListNested : 

    def __init__(self):
        self._setup()

    def _setup(self):
        self.current = "" 
        self.result = []

    def process_nested_liest(self, list_in_string:str):
        for ch in list_in_string:
            if ch == "[":
                self._add(None)
                self.result.append(["StartList"])
            elif ch == "]":
                self._add(None)
                self.result.append(["EndList"])
            else:
                self.current += ch
        
        return self.result
    
    def _add(self, thing):
        if len(self.current) > 0:
            self.result.append(["Lit", self.current])
            self.current = ""
        
        if thing is not None:
            self.result.append([thing])

