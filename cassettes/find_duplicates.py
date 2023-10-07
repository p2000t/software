import os
import hashlib

#
# Purpose
#
# Find duplicate .cas files which have different names, but the same MD5 hash
#

def main():

    checksums = []
    paths = [] # store list of file paths

    for root, dirs, files in os.walk('.'):
        for file in files:
            path = os.path.join(root, file)
            if os.path.splitext(path)[1].lower() == ".cas":
                with open(path, "rb") as f:
                    bytes = bytearray(f.read())
                    # ignore headers by clearing them
                    for i in range(len(bytes) - 1):
                        if i % (256+1024) < 256:
                            bytes[i] = 0
                    checksum = hashlib.md5(bytes).hexdigest()
                    if checksum in checksums:
                        otherPath = paths[checksums.index(checksum)]
                        print('\n[ERROR] Duplicate .cas files found: "%s" and "%s"' % (path, otherPath))
                        return
                    else:
                        print('Checked "%s"' % path)
                        checksums.append(checksum)
                        paths.append(path)

    print("\nNo duplicates found. You're good to go!")

if __name__ == '__main__':
    main()    