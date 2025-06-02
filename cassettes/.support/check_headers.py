import os
import math
import hashlib

#
# Purpose
#
# Find .cas files with invalid headers
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
    
    counter = 0
    # check CAS headers
    for path in paths:
        [valid, prog_type] = check_cartridge_header(path)
        if not valid:
            counter += 1
            print(f'{counter:03d} ({"Single prog" if prog_type == 1 else "Multi prog" }) Fixed invalid CAS header: %s' % path)

    print("\n...done!")

def check_cartridge_header(path):
    """
    Parse the cartridge header metadata and check whether each consecutive 
    recnum whose previous recnum is not 1 should be
          one smaller than the previous recnum
    
    Returns parsing check (true/false) and list of errors
    """
    with open(path, 'rb') as f:
        data = bytearray(f.read())

    # calculate number of blocks
    nrblocks = len(data) // 0x500

    num_bytes_loc = 0x500 + 0x34
    num_bytes = int.from_bytes(data[num_bytes_loc:num_bytes_loc+2], byteorder='little')
    if math.ceil(num_bytes / 1024) == nrblocks:
        prog_type=1
    else:
        prog_type=2

    prev_recnum = 1
    valid = True
    
    # loop over blocks
    for i in range(nrblocks):
        # check if number of remaining blocks is valid
        recnum = data[i * 0x500 + 0x4F]
        
        # check if the record number is one smaller than previous record number
        if prev_recnum != 1 and recnum != prev_recnum-1:
            valid = False
        prev_recnum = recnum

    # if not valid and prog_type == 1:
        
    #     # fix the header
    #     for i in range(nrblocks):
    #         data[i * 0x500 + 0x4F] = nrblocks - i
    #     # and save the file
    #     with open(path, 'wb') as f:
    #         f.write(data)

    return [valid, prog_type]

if __name__ == '__main__':
    main()    