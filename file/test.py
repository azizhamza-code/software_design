import pytest
import pyfakefs
import file
from pathlib import Path
from file import hash_all, HASH_LEN, Archive
from unittest.mock import patch
import os
from file import get_index
from file import ArchiveIndex

@pytest.fixture
def our_fs_1(fs):
    fs.create_file("a.txt", contents="aaa")
    fs.create_file("b.txt", contents="bbb")
    fs.create_file("sub_dir/c.txt", contents="ccc")

def test_hashing(our_fs_1):
    result = hash_all(".")
    expected = {"a.txt", "b.txt", "sub_dir/c.txt"}
    assert {r[0] for r in result} == expected
    assert all(len(r[1]) == HASH_LEN for r in result)

def test_change(our_fs_1):
    original = hash_all(".")
    original = [entry for entry in original if entry[0] == "a.txt"][0]
    with open("a.txt", "w") as writer:
        writer.write("this is new content for a.txt")
    changed = hash_all(".")
    changed = [entry for entry in changed if entry[0] == "a.txt"][0]
    assert original != changed


FILES = {"a.txt": "aaa", "b.txt": "bbb", "sub_dir/c.txt": "ccc"}
BACKUP_DIR_MANIFEST_FILE = {"0000001.csv": "242324", "0000002.csv": "242325"}
backup_dir = "/backup"

@pytest.fixture
def our_fs(fs):
    for name, contents in FILES.items():
        fs.create_file(name, contents=contents)
    if not Path(backup_dir).exists():
        Path(backup_dir).mkdir()
    for name, contents in BACKUP_DIR_MANIFEST_FILE.items():
        fs.create_file(Path(backup_dir, name), contents=contents)


def test_our_fs(our_fs):
    backup_file_name = os.path.join('/backup', "0000001.csv")
    assert Path(backup_file_name).exists

def test_index(our_fs):
    assert get_index(backup_dir) == "0000000003"


def test_nested_example(our_fs):
    timestamp = 1234
    with patch("file.current_time", return_value=timestamp):
        backup = Archive(".")
        manifest = backup.backup("/backup")
    assert Path("/backup", f"{timestamp}.csv").exists()
    for filename, hash_code in manifest:
        assert Path("/backup", f"{hash_code}.bck").exists()

def test_the_nex_archive_index(our_fs):
    next_index = "0000000003"
    with patch("file.get_index", return_value=next_index):
        backup = ArchiveIndex(".")
        manifest = backup.backup("/backup")
        assert Path("/backup", f"{next_index}.csv").exists()
    for filename, hash_code in manifest:
        assert Path("/backup", f"{hash_code}.bck").exists()