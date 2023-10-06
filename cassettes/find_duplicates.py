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
    duplicates_found = False

    for root, dirs, files in os.walk('.'):
        for file in files:
            path = os.path.join(root, file)
            if os.path.splitext(path)[1].lower() == ".cas":
                with open(path, "rb") as f:
                    checksum = hashlib.md5(f.read()).hexdigest()
                    if checksum in checksums:
                        otherPath = paths[checksums.index(checksum)]
                        print('Duplicate .cas files found: "%s" and "%s"' % (path, otherPath))
                        duplicates_found = true     
                    else:
                        checksums.append(checksum)
                        paths.append(path)

    if not duplicates_found:
        print("No duplicates found. You're good to go!") 

if __name__ == '__main__':
    main()    