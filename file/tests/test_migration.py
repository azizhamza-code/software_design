import pytest
from pathlib import Path
from ..file import manifest_migration, migration_old_manifest_to_new_format, read_csv_manifet

MOCK_CSV_MANIFEST_CONTENTS = {
    "0000001.csv": (
        "filename,hash\n" 
        "data/file1.txt,hash123abc\n"
        "another_file.py,hash456def"
    ),
    "0000002.csv": (
        "filename,hash\n"
        "image.jpg,hash789ghi\n"
        "notes/document.txt,hash012jkl"
    )
}

@pytest.fixture
def fs_with_csv_manifest(fs):
    test_backup_dir = "/test_backup_for_migration"
    for name, csv_string_content in MOCK_CSV_MANIFEST_CONTENTS.items():
        fs.create_file(Path(test_backup_dir, name), contents=csv_string_content)
    return test_backup_dir


def test_migration_old_manifest_to_new_format(fs_with_csv_manifest):
    backup_path = fs_with_csv_manifest
    migration_old_manifest_to_new_format(backup_path)
    assert "user_name" in read_csv_manifet

import json

def test_json_migration(fs_with_csv_manifest):
    bachup_path = fs_with_csv_manifest
    manifest_migration(bachup_path)
    assert Path(bachup_path, "0000001.json").exists()
    with open(Path(bachup_path, "0000001.json"), "r") as json_read :
        d = json.load(json_read)
        assert d["data/file1.txt"] == "hash123abc"