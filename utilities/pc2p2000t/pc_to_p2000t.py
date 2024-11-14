#
# pc_to_p2000t.py 
#
#   This Python script sends one or multiple .cas files via RS-232 to a Philips P2000T Computer.
#   The P2000T must be connected to the PC via a serial cable or a "USB to RS232 serial adapter" and
#   running the utility "pc2p2000t.bas" in receive-store ("ontvang-bewaar") mode. Make sure the target
#   cassette is empty and pc2p2000t is started [Basic commmand: ?USR2(0)] before running this script.
#
# example:
#   python pc_to_p2000t.py COM4 /path/to/file1.cas /path/to/file2.cas
#
# for Linux or Mac, use e.g. /dev/ttyUSB3 instead of COM4
#

import os
import sys
import argparse
import time
import subprocess

try:
    import serial
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'pyserial'])
    import serial

def send_file_to_serial(file_path, serial_port, is_last_file):
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension != '.cas':
        print(f'Error: unsupported file extension for "{file_path}"')
        return 

    # Open the input file in read mode
    with open(file_path, 'rb') as file:
        # Read the first block of the first program file in this .cas
        # Each block contains 256 header bytes + 1024 data bytes
        first_block = file.read(256 + 1024)

        while True:
            if not first_block:
                break

            # Put the block of P2000T file data into a byte array
            block_data = bytearray(first_block)

            # Get the total number of file blocks from the block's header
            p2000_file_block_count = block_data[0x4F]

            # Get the file name from the block's header
            p2000_file_name = block_data[0x36:0x36+8] + block_data[0x47:0x47+8]
            p2000_file_name = p2000_file_name.decode('ascii', errors='ignore').rstrip()

            p2000_file_type = block_data[0x41]
            # If the P2000 file type is a stand-alone program ('P') then change the transfer-address 
            # in the header to 0x6547 to prevent that pc2p2000t loads the progam into memory which 
            # is unavailable without a memory expansion (&HA000 - &HFFFF)
            if p2000_file_type == 0x50: # 'P'
                block_data[0x30] = 0x47
                block_data[0x31] = 0x65
                
            # Read the remaining blocks for the P2000T file
            for _ in range(p2000_file_block_count - 1):
                next_block = file.read(256 + 1024)
                if not next_block:
                    print(f'Error: missing block(s) for P2000T file "{p2000_file_name}"')
                    return
                block_data.extend(bytearray(next_block))

            # Send the P2000T file blocks to the serial port
            print(f'Sending P2000T file "{p2000_file_name}" ({p2000_file_block_count} blocks)...')
            serial_port.write(block_data)
            serial_port.flush()

            # Read the first block of the next program file in this .cas
            first_block = file.read(256 + 1024)

            if first_block or not is_last_file:
                # Now wait for 10 seconds (=cassette ramp-up time) + 2 times the number of blocks,
                # which allows the P2000T to save the received file to cassette tape
                sleep_seconds = 10 + 2 * p2000_file_block_count
                print(f'Waiting for {sleep_seconds} seconds while P2000T saves to cassette...')
                time.sleep(sleep_seconds)

if __name__ == '__main__':

    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_port", help="Serial I/O port connected to the P2000T. E.g. COM4 (for Windows) or /dev/ttyUSB3 (for Linux and macOS)")
    parser.add_argument("file_path", nargs='+', help="Path(s) to the .cas file(s)")
    
    # Parse arguments
    args = parser.parse_args()

    try:
        # Create serial port with the specified settings
        serial_port = serial.Serial(
            port=args.serial_port,
            baudrate=9600, 
            parity=serial.PARITY_NONE, 
            stopbits=serial.STOPBITS_ONE, 
            bytesize=serial.EIGHTBITS)

        # Call the function to send each .cas/.p2000t file to the serial port
        for index, file_path in enumerate(args.file_path):
            is_last_file = (index == len(args.file_path) - 1)
            send_file_to_serial(file_path, serial_port, is_last_file)
        print('Done!')

    finally:
        if serial_port.is_open:
            serial_port.close()
