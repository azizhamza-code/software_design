from pathlib import Path
import glob
import csv
import json

def manifest_migration_csv_to_json(backup_dir):
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

def read_csv_manifet(path_file)->dict:
    dict_file = {}
    with open(path_file, "r") as csv_file:
        reader:csv._reader = csv.reader(csv_file)
        for file_name, hash  in reader:
            if file_name != "filename":
                dict_file[file_name] = hash
    return dict_file

def migration_old_manifest_to_new_format(backup_dir):
    for file in glob.glob("**/*.csv", root_dir=backup_dir, recursive=True):
        path_file = Path(backup_dir, file)
        manifest = read_csv_manifet(path_file=path_file)
        json_path_file = Path(backup_dir, file.replace("csv", "json"))
        with open(json_path_file, "w") as json_writer : 
            json.dump(dict_file, json_writer)