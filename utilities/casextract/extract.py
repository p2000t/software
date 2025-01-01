import sys

def process_cas_file(input_file_path, output_file_path):
    header_size = 256
    data_size = 1024
    program_size = None
    output_data = bytearray()

    with open(input_file_path, 'rb') as input_file:
        while True:
            block = input_file.read(header_size + data_size)
            if not block:
                break
            if not program_size:
                program_size = int.from_bytes(block[0x34:0x36], byteorder='little')
                print ("Program size: %d" % program_size)
            output_data.extend(block[-data_size:])

    with open(output_file_path, 'wb') as output_file:
        output_file.write(output_data[:program_size])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    process_cas_file(input_file_path, output_file_path)