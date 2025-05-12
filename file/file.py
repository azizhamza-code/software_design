import glob
from pathlib import Path
import hashlib
HASH_LEN = 16

def hash_all(root):
    result = []
    for name in glob.glob("**/*.*", root_dir=root, recursive=True):
        full_name = Path(root, name)
        with open(full_name, "rb") as reader:
            data = reader.read()
            hash_code = hashlib.sha256(data).hexdigest()[:HASH_LEN]
            result.append((name, hash_code))
    return result




