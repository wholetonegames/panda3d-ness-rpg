import hashlib
from panda3d.core import (VirtualFileSystem,
                          Multifile,
                          Filename)


def md5_sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def md5_contents(filename):
    m = Multifile()
    m.openRead(filename)
    payload = []
    for i in range(m.getNumSubfiles()):
        payload.append(m.get_subfile_name(i))
    m.close()
    return payload


if __name__ == "__main__":
    m = 'assets.mf'
    print(md5_sum(m))
    for x in md5_contents(m):
        print(x)
