import pytest
import pyfakefs
from pathlib import Path
from ..file import Archive
from unittest.mock import patch

@pytest.fixture
def our_fs_1(fs):
    fs.create_file("a.txt", contents="aaa")
    fs.create_file("b.txt", contents="bbb")
    fs.create_file("sub_dir/c.txt", contents="ccc")

def test_name_in_manifest(our_fs_1):
    user_name = 'test'
    backup_dir = "/backup"
    with patch('software_design.file.file.getpass.getuser', return_value=user_name), patch('software_design.file.file.current_time', return_value='3'):
        archive = Archive(".")
        manifest = archive.backup(backup_dir, format="csv")
    path = Path("/backup", "3.csv")
    with open (path, "r") as manifest_csv_reader:
        lines = manifest_csv_reader.readlines()
        for line in lines :
            key = line.split(',')[0].strip()
            if key == 'user_name':
                assert line.split(',')[1].strip() == 'test'

