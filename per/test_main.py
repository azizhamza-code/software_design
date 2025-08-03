from main import DfRow

def test_filter():
    
    given = [
        {
            "a":4,
            "b":5
        },
        {
            "a":3,
            "b":5
        },

            ]
    
    df = DfRow(given)

    def is_a_column_even(row):
        if 'a' in row and row['a'] % 2 == 0:
            return True
        return False
    
    df = df.filter(is_a_column_even)
        
    expected = [
        {
            "a":4,
            "b":5
        }
            ]
    
    assert df.eq(DfRow(expected))
