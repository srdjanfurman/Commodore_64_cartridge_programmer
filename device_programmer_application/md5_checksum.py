"""
Created on Jun 20, 2017

@author: sfurman
"""

import hashlib


# Currently not in use.
def md5_checksum(file_path):
    with open(file_path, 'rb') as f:
        m = hashlib.md5()
        while True:
            # The file is read in 8192-byte chunks.
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()
