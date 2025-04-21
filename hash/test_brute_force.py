import os
import tempfile
import pytest
from brute_force import find_groups

def test_find_groups_with_mock_data():
    contents = [b"hello world", b"hello world", b"different"]
    temp_files = []
    try:
        for content in contents:
            fd, path = tempfile.mkstemp()
            with os.fdopen(fd, 'wb') as f:
                f.write(content)
            temp_files.append(path)
        groups = find_groups(temp_files, chunk_size=4)
        group_sizes = sorted(len(g) for g in groups.values())
        assert group_sizes == [1, 2]
        grouped = [sorted(list(g)) for g in groups.values() if len(g) == 2][0]
        assert set(grouped) == set(temp_files[:2])
    finally:
        for path in temp_files:
            os.remove(path) 