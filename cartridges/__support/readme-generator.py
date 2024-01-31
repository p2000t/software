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
    out += "| Name | Code | Description | MD5 checksum |\n"
    out += "| ---- | ---- | ----------- | ------------ |\n"
    
    for cart in data['cartridges']:
        # calculate checksum
        f = open("../" +cart['filename'], 'rb')
        checksum = hashlib.md5(f.read()).hexdigest()
        f.close()
        
        icon = ":floppy_disk:"
        
        out += "| [%s](%s) | %s | %s | `%s` |\n" % (cart['name'],
                                               urllib.parse.quote(cart['filename']),
                                               cart['code'] if "code" in cart else "",
                                               cart['description'],
                                               checksum)
        
    with open("../README.md", 'w') as f:
        f.write(out)

def check_files(data):
    """
    Verify whether all files are present and checks for duplicates based
    on the MD5 checksum
    """
    checksums = []
    filenames = [] # store list of file names
    
    for file in data['cartridges']:
        filename = file['filename']
        filenames.append(filename)
        if os.path.exists("../" + filename):
            print('%s [OK]' % filename)
            with open("../" + filename, 'rb') as f:
                checksum = hashlib.md5(f.read()).hexdigest()
                if checksum in checksums:
                    raise Exception('Duplicate file found: %s' % filename)        
                else:
                    checksums.append(checksum)
        else:
            raise Exception('File %s not found!' % filename)

    # additionally check whether there are any files in the folder which
    # are not represented in the json file
    root = os.path.dirname(os.path.dirname(__file__))
    for path in os.listdir(root):
        if os.path.isfile(os.path.join(root, path)) and \
           os.path.splitext(os.path.join(root, path))[1].lower() == '.bin':
            if path not in filenames:
                print(path)
                print('[WARNING] File %s is not listed in cartridges.json.' % path)

if __name__ == '__main__':
    main()    