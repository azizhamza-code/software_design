import time 

def all_eq(*values):
    return (not values) or all(v == values[0] for v in values)

class DataFrame:
    def ncol(self):
        """Report the number of columns."""

    def nrow(self):
        """Report the number of rows."""

    def cols(self):
        """Return the set of column names."""

    def eq(self, other):
        """Check equality with another dataframe."""

    def get(self, col, row):
        """Get a scalar value."""

    def select(self, *names):
        """Select a named subset of columns."""

    def filter(self, func):
        """Select a subset of rows by testing values."""
class DfRow(DataFrame):
    def __init__(self, rows):
        assert len(rows) > 0
        assert all(dict_match(r, rows[0]) for r in rows)
        self._data = rows

    def ncol(self):
        return len(self._data[0])
    
    def nrow(self):
        return len(self._data)
    
    def cols(self):
        return set(self._data[0].keys())
    
    def get(self, col, row):
        assert col in self._data[0]
        assert 0 <= row < len(self._data)
        return self._data[row][col]
    
    def eq(self, other):
        assert isinstance(other, DataFrame)
        for (i, row) in enumerate(self._data) :
            for key in row:
                if key not in other.cols():
                    return False
                if row[key] != other.get(key, i):
                    return False
        return True
        
    def select(self, *names):
        assert all(n in self._data[0] for n in names)
        rows = [{key: r[key] for key in names} for r in self._data]
        return DfRow(rows)
    
    def filter(self, func):
        result = [r for r in self._data if func(**r)]
        return DfRow(result)

    def toColRow(self):
        """ col format is the following dict with key : value (list)
            row format is in the forme of : [{k (col), v }]
        """
        def get_col_list(k):
            l = []
            for r in range(self.nrow()):
                l.append(self.get(k, r))
            return l
    
        return DfCol(** {
            k : get_col_list(k) for k in self.cols()
        })
        
    
def dict_match(d, prototype):
    if set(d.keys()) != set(prototype.keys()):
        return False
    return all(type(d[k]) == type(prototype[k]) for k in d)


def match(rows, schema):
    return set(rows[0].keys()) == set(schema) if rows else True

class DfrowE(DfRow):
    def __init__(self, rows: list[dict], schema: list[str]):
        self._cols = list(schema)
        if rows:
            assert match(rows, schema)
            super().__init__(rows)  # validate and set _data
        else:
            self._data = []         # represent empty rows

    def ncol(self):
        return len(self._cols)

    def cols(self):
        return set(self._cols)

    def select(self, *names):
        assert all(n in self._cols for n in names)
        projected = [{k: r[k] for k in names} for r in self._data]
        return DfrowE(projected, list(names))

    def filter(self, func):
        filtered = [r for r in self._data if func(**r)]
        return DfrowE(filtered, self._cols)

    def eq(self, other):
        if not isinstance(other, DataFrame):
            return False
        if self.cols() != other.cols():
            return False
        # reuse DfRow.eq behavior for values
        for i, row in enumerate(self._data):
            for k, v in row.items():
                if v != other.get(k, i):
                    return False
        return True
        
class DfCol(DataFrame):
    def __init__(self, **kwargs) -> None:
        assert len(kwargs) > 0 
        assert all_eq(len(kwargs[k]) for k in kwargs)
        for k in kwargs:
            assert all_eq(type(v) for v in kwargs[k])
        self._data = kwargs
    def ncol(self):
        return len(self._data)

    def nrow(self):
        n = list(self._data.keys())[0]
        return len(self._data[n])

    def cols(self):
        return set(self._data.keys())

    def get(self, col, row):
        assert col in self._data
        assert 0 <= row < len(self._data[col])
        return self._data[col][row]

    def eq(self, other):
        assert isinstance(other, DataFrame)
        for n in self._data:
            if n not in other.cols():
                return False
            for i in range(len(self._data[n])):
                if self.get(n, i) != other.get(n, i):
                    return False
        return True
    
    def select(self, *names):
        assert all(n in self._data for n in names)
        return DfCol(**{n: self._data[n] for n in names})
    
    def filter(self, func):
        result = {n: [] for n in self._data}
        for i in range(self.nrow()):
            args = {n: self._data[n][i] for n in self._data}
            if func(**args):
                for n in self._data:
                    result[n].append(self._data[n][i])
        return DfCol(**result)
    


RANGE = 10

def make_col(nrow, ncol):
    def _col(n, start):
        return [((start + i) % RANGE) for i in range(n)]
    fill = {f"label_{c}": _col(nrow, c) for c in range(ncol)}
    return DfCol(**fill)

def make_row(nrow, ncol):
    labels = [f"label_{c}" for c in range(ncol)]
    def _row(r):
        return {
            c: ((r + i) % RANGE) for (i, c) in enumerate(labels)
        }
    fill = [_row(r) for r in range(nrow)]
    return DfRow(fill)

FILTER = 2


def time_filter(df):
    def f(label_0, **args):
        return label_0 % FILTER == 1
    start = time.time()
    df.filter(f)
    return time.time() - start


SELECT = 3

def time_select(df):
    indices = [i for i in range(df.ncol()) if ((i % SELECT) == 0)]
    labels = [f"label_{i}" for i in indices]
    start = time.time()
    df.select(*labels)
    return time.time() - start

def make_cold(nrow, ncol):
    def _col(n, start):
        return [((start + i) % RANGE) for i in range(n)]
    fill = {f"label_{c}": _col(nrow, c) for c in range(ncol)}
    return DfcolD(**fill)

def time_filter_efficient(df):
    def f(label_0):
        return label_0 % FILTER == 1
    start = time.time()
    df.filter(f)
    return time.time() - start

def sweep(sizes):
    result = []
    for (nrow, ncol) in sizes:
        df_col = make_col(nrow, ncol)
        df_row = make_row(nrow, ncol)
        df_cold = make_cold(nrow, ncol)
        times = [
            time_filter(df_col),
            time_select(df_col),
            time_filter(df_row),
            time_select(df_row),
            time_filter_efficient(df_cold),
        ]
        result.append([nrow, ncol, *times])
    return result


from inspect import signature
class DfcolD(DfCol):
    """dict of list"""
    def filter(self, func):
        params = get_col(func)
        result = {n: [] for n in self._data}
        for i in range(self.nrow()):
            args_for_func = {}
            for p in params:
                if p == 'i_row':
                    args_for_func['i_row'] = i
                else:
                    args_for_func[p] = self._data[p][i]
            if func(**args_for_func):
                for n in self._data:
                    result[n].append(self._data[n][i])
        return DfcolD(**result)
    
def get_col(func):
    sig = signature(func)
    return list(sig.parameters.keys())

if __name__ == '__main__':
    sizes = [(10, 10), (100, 100), (1000, 1000), (10000, 100)]
    results = sweep(sizes)
    print("nrow\tncol\tfilter col\tselect col\tfilter row\tselect row\tfilter eff")
    for r in results:
        print(f"{r[0]}\t{r[1]}\t{r[2]:.6f}\t{r[3]:.6f}\t{r[4]:.6f}\t{r[5]:.6f}\t{r[6]:.6f}")
