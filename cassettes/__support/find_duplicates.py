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

    # collecting all files and checking for duplicates
    for root, dirs, files in os.walk('..'):
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
        for error in errorlist:
            print('\t%s' % error)
        
    print('Invalid CAS: %i / %i' % (len(invalid_header), len(paths)))

def check_cartridge_header(path):
    """
    Parse the cartridge header metadata and check whether number of blocks
    and file sizes match
    
    Checks:
        * Recnum [0x4F] should lie between 1-40, inclusive
        * Each consecutive recnum whose previous recnum is not 1 should be
          one smaller than the previous recnum
        * The filesize should never exceed the number of blocks multiplied by 
    
    Returns parsing check (true/false) and list of errors
    """
    f = open(path, 'rb')
    data = f.read()
    f.close()
    
    errorlist = []
    valid_flag = True
    
    # calculate number of blocks
    nrblocks = len(data) // 0x500
    prev_recnum = 1
    
    # loop over blocks
    for i in range(nrblocks):
        # check if number of remaining blocks is valid
        recnum = data[i * 0x500 + 0x4F]
        if not (recnum >= 1 or recnum <= 40):
            errorlist.append('B%02i: Invalid recum found: %i' % (i,recnum))
            valid_flag = False
        
        # check if the record number is one smaller than previous record number
        # skip this check if the previous recnum was 1
        if prev_recnum != 1:
            if recnum != prev_recnum-1:
                errorlist.append('B%02i: Invalid sequence in recnum %i > %i' % (i,recnum, prev_recnum))
                valid_flag = False
        prev_recnum = recnum

        # determine filesize and record length
        # note big endian format
        filesize = data[i * 0x500 + 0x33] * 256 + data[i * 0x500 + 0x32]
        record_length = data[i * 0x500 + 0x35] * 256 + data[i * 0x500 + 0x34]
        
        # check if filesize lies between boundaries
        if filesize > nrblocks * 0x400:
            errorlist.append('B%02i: Filesize (%i) does not match number of blocks (%i)' 
                             % (i,filesize, nrblocks))
            valid_flag = False

    return valid_flag, errorlist

if __name__ == '__main__':
    main()    