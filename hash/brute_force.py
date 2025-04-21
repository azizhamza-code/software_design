import sys
from hashlib import sha256

def find_groups(filenames, chunk_size=4):
    groups = {}
    for fn in filenames:
        hash_code = sha256()
        with open(fn, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                hash_code.update(chunk)
        digest = hash_code.hexdigest()
        if digest not in groups:
            groups[digest] = set()
        groups[digest].add(fn)
    return groups


if __name__ == "__main__":
    groups = find_groups(sys.argv[1:])
    for filenames in groups.values():
        print(", ".join(sorted(filenames)))