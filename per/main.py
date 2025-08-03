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
                if row[key] != other.get(key, i)
                return False
        return True
        
    def select(self, *names):
        assert all(n in self._data[0] for n in names)
        rows = [{key: r[key] for key in names} for r in self._data]
        return DfRow(rows)

def dict_match(d, prototype):
    if set(d.keys()) != set(prototype.keys()):
        return False
    return all(type(d[k]) == type(prototype[k]) for k in d)

