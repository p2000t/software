import os
import hashlib

#
# Purpose
#
# Find duplicate .cas files which have different names, but the same MD5 hash
#

def main():

    print("\nStarting CAS header check...")

    paths = [] # store list of file paths

    # collecting all files and checking for duplicates
    for root, dirs, files in os.walk('..'):
        for file in files:
            path = os.path.join(root, file)
            if os.path.splitext(path)[1].lower() == ".cas":
                paths.append(path)
    
    # check CAS headers
    for path in paths:
        if not check_cartridge_header(path):
            print('Invalid CAS header: %s' % path)

    print("\n...done!")

def check_cartridge_header(path):
    """
    Parse the cartridge header metadata and check whether each consecutive 
    recnum whose previous recnum is not 1 should be
          one smaller than the previous recnum
    
    Returns parsing check (true/false) and list of errors
    """
    with open(path, 'rb') as f:
        data = f.read()

    # calculate number of blocks
    nrblocks = len(data) // 0x500
    prev_recnum = 0
    
    # loop over blocks
    for i in range(nrblocks):
        # check if number of remaining blocks is valid
        recnum = data[i * 0x500 + 0x4F]

        # check if the record number is one smaller than previous record number
        if prev_recnum > 1 and recnum != prev_recnum-1:
            return False
        prev_recnum = recnum

    return True

if __name__ == '__main__':
    main()    