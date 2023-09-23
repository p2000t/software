import json
import os
import hashlib
import urllib.parse

#
# Purpose
#
# Parses "cartridges.json" to build the README.md file.
#

def main():
    with open('cartridges.json', 'r') as f:
        data = json.load(f)
        
    check_files(data)
    build_readme(data)

def build_readme(data):
    """
    Build (formatted) README.md file based on cartridges.json
    """
    out = "# Cartridges\n\n"
    out += "|    | Cart name | Description | MD5 checksum |\n"
    out += "| --- | --------- | ----------- | ----------- |\n"
    
    for cart in data['cartridges']:
        # calculate checksum
        f = open(cart['filename'], 'rb')
        checksum = hashlib.md5(f.read()).hexdigest()
        f.close()
        
        icon = ":floppy_disk:"
        
        out += "| %s | [%s](%s) | %s | `%s` |\n" % (icon,
                                                    cart['name'],
                                                    urllib.parse.quote(cart['filename']),
                                                    cart['description'],
                                                    checksum)
        
    with open("README.md", 'w') as f:
        f.write(out)

def check_files(data):
    """
    Verify whether all files are present and checks for duplicates based
    on the MD5 checksum
    """
    checksums = []
    
    for file in data['cartridges']:
        filename = file['filename']
        if os.path.exists(filename):
            print('%s [OK]' % filename)
            with open(filename, 'rb') as f:
                checksum = hashlib.md5(f.read()).hexdigest()
                if checksum in checksums:
                    raise Exception('Duplicate file found: %s' % filename)        
                else:
                    checksums.append(checksum)
        else:
            raise Exception('File %s not found!' % filename)

if __name__ == '__main__':
    main()    