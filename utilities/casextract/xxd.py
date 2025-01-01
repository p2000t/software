import sys

def binary_to_z80_source(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as input_file:
        binary_data = input_file.read()

    with open(output_file_path, 'w') as output_file:
        for i in range(0, len(binary_data), 12):
            chunk = binary_data[i:i+12]
            hex_values = ', '.join(f'0x{byte:02X}' for byte in chunk)
            output_file.write(f'    DB {hex_values}\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python xxd.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    binary_to_z80_source(input_file_path, output_file_path)