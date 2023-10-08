import os
import hashlib
import numpy as np

#
# Purpose
#
# Find duplicate .cas files which have different names, but the same MD5 hash
#

def main():

    checksums = []
    paths = [] # store list of file paths

    # collecting all files and checking for duplicates
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
    print() # additional whiteline
    
    # check CAS headers
    invalid_header = []
    errorlists = []
    for path in paths:
        [flag_valid, errorlist] = check_cartridge_header(path)
        if not flag_valid:
            invalid_header.append(path)
            errorlists.append(errorlist)
            
    print('The following CAS files have invalid headers:')
    for i,(path,errorlist) in enumerate(zip(invalid_header, errorlists)):
        print('%03i: %s (%i header errors)' % (i+1, path, len(errorlist)))
        
    print('Invalid CAS: %i / %i' % (len(invalid_header), len(paths)))
    
    #print(errorlists[45])

def check_cartridge_header(path):
    """
    Parse the cartridge header metadata and check whether number of blocks
    and file sizes match
    
    Returns parsing check (true/false) and list of errors
    """
    f = open(path, 'rb')
    data = f.read()
    f.close()
    
    errorlist = []
    valid_flag = True
    
    # calculate number of blocks
    nrblocks = len(data) // 0x500
    
    # loop over blocks
    for i in range(nrblocks):
        # check if number of remaining blocks is valid
        if np.uint8(data[i * 0x500 + 0x4F]) != np.uint8(nrblocks - i):
            errorlist.append('[Block %i] Incorrect block value: %i != %i' 
                             % (i, data[i * 0x500 + 0x4F], nrblocks - i - 1))
            valid_flag = False

        # determine filesize and record length
        # note big endian format
        filesize = data[i * 0x500 + 0x33] * 255 + data[i * 0x500 + 0x32]
        record_length = data[i * 0x500 + 0x35] * 255 + data[i * 0x500 + 0x34]
        
        # check if filesize lies between boundaries
        if not (filesize > (nrblocks-1) * 0x400 and filesize <= nrblocks * 0x400):
            errorlist.append('[Block %i] Filesize (%i) does not match number of blocks (%i)' 
                             % (i, filesize, nrblocks))
            valid_flag = False
        
        # check if record length lies between boundaries
        if not (record_length > (nrblocks-1) * 0x400 and filesize <= nrblocks * 0x400):
            errorlist.append('[Block %i] Record length (%i) does not match number of blocks (%i)' 
                             % (i, record_length, nrblocks))
            valid_flag = False
            
        # check if filesize matches record length
        if filesize != record_length:
            errorlist.append('[Block %i] Filesize (%i) does not match record length (%i)' 
                             % (i, filesize, record_length))
            valid_flag = False

    return valid_flag, errorlist

if __name__ == '__main__':
    main()    