import glob
import json
from pathlib import Path
import hashlib
from time import time
import csv
import shutil

HASH_LEN = 16
INDEX_LEN = 10

class NotRightFormat(Exception):
    pass

def current_time():
    return f"{time.time()}".split(".")[0]

def get_index(backup_dir)->str:
    files = glob.glob("**/*.{csv}", root_dir=backup_dir, recursive=True)
    files_index = [int(file.split(".csv")[0]) for file in files]
    current_index= max(files_index)
    return '0' * (INDEX_LEN - len(str(current_index + 1))) + str(current_index + 1)

def manifest_migration(backup_dir):
    for file in glob.glob("**/*.csv", root_dir= backup_dir, recursive=True):
        path_file = Path(backup_dir, file)
        dict_file = {}
        with open(path_file, "r") as csv_file:
            reader:csv._reader = csv.reader(csv_file)
            for file_name, hash  in reader:
                if file_name != "filename":
                    dict_file[file_name] = hash
        json_path_file = Path(backup_dir, file.replace("csv", "json"))
        with open(json_path_file, "w") as json_writer : 
            json.dump(dict_file, json_writer)

                

def list_of_tupe_to_dict(data)-> dict:
    return {k:v for (k,v) in data}
    
def hash_all(root):
    result = []
    for name in glob.glob("**/*.*", root_dir=root, recursive=True):
        full_name = Path(root, name)
        with open(full_name, "rb") as reader:
            data = reader.read()
            hash_code = hashlib.sha256(data).hexdigest()[:HASH_LEN]
            result.append((name, hash_code))
    return result

class Archive:
    def __init__(self, source_dir):
        self.source_dir = source_dir

    def backup(self, backup_dir, format = "csv"):
        manifest = hash_all(self.source_dir)
        timestemp = current_time()
        self._write_manifest(backup_dir, timestemp, manifest, format)
        self._copy_files(self.source_dir, backup_dir, manifest)
        return manifest
    
    def _write_manifest(self, backup_dir, timestemp, manifest, format = "csv"):
        backup_dir = Path(backup_dir)
        if not backup_dir.exists():
            backup_dir.mkdir()
        if format == "csv":
            manifest_file = Path(backup_dir, f"{timestemp}.csv")
            with open(manifest_file, "w") as raw:
                writer = csv.writer(raw)
                writer.writerow(["filename", "hash"])
                writer.writerows(manifest)
        elif format =="json": 
            manifest_file = Path(backup_dir, f"{timestemp}.json")
            with open(manifest_file, "w") as raw:
                json.dump(list_of_tupe_to_dict(manifest), raw)

    def _copy_files(self, source_dir, backup_dir, manifest):
        for (file_name, hash_code) in manifest:
            source_path = Path(source_dir, file_name)
            backup_path = Path(backup_dir, f"{hash_code}.bck")
            if not backup_path.exists():
                shutil.copy(source_path, backup_path)

class ArchiveIndex(Archive):
    def __init__(self, source_dir):
        super().__init__(source_dir)

    def backup(self, backup_dir, format = "csv"):
        manifest = hash_all(self.source_dir)
        index = get_index(backup_dir)
        self._write_manifest(backup_dir, index, manifest, format)
        self._copy_files(self.source_dir, backup_dir, manifest)
        return manifest
    




            
        