#
# sendcas.py - A Python script to send one or multiple .cas files via RS-232 to a Philips P2000T computer
#              The P2000T must be connected to the PC by a "USB to RS232 serial adapter" and running 
#              the program "pc2p2000t" in receive-store mode. Please make sure the target cassette is 
#              empty and pc2p2000t is running (use ?USR2(0)) before running this script.
#
# run the script from the command line like this:
#   python sendcas.py /path/to/file1.cas /path/to/file2.cas /path/to/file3.cas COM4
#
# for Linux or Mac, use e.g. /dev/ttyUSB3 instead of COM4
#

import serial
import argparse
import time

BLOCK_SIZE = 256 + 1024 # 256 bytes header + 1024 bytes data
HEADER_START = 0x30     # record info offset from begin of block

def send_cas_to_serial(cas_file, serial_port):
    # Open the .cas file in read mode
    with open(cas_file, 'rb') as file:
        # Read the file in blocks of 1280 bytes 
        while True:
            first_block = file.read(BLOCK_SIZE)
            if not first_block:
                break

            # Accumulate the blocks of progam data into a byte array
            program_data = bytearray(first_block)

            # Get the total number of program blocks from the block header
            program_total_blocks = first_block[HEADER_START + 0x1F]

            # Get the program name from the block's header
            program_name = first_block[HEADER_START+0x06:HEADER_START+0x06+8] + first_block[HEADER_START+0x17:HEADER_START+0x17+8]
            program_name = program_name.decode('ascii', errors='ignore').rstrip()

            program_type = first_block[HEADER_START + 0x11]
            # If the program type is a stand-alone program ('P') then change the transfer-address 
            # in the header to 0x6547 to prevent that pc2p2000t loads the progam into memory which 
            # is unavailable without a memory expansion (&HA000 - &HFFFF)
            if program_type == 0x50: # 'P'
                program_data[HEADER_START + 0x00] = 0x47
                program_data[HEADER_START + 0x01] = 0x65
                
            # Read the remaining blocks of the program
            for _ in range(program_total_blocks - 1):
                next_block = file.read(BLOCK_SIZE)
                if not next_block:
                    break
                program_data.extend(next_block)

            # Print the program name
            print(f'Sending program "{program_name}" ({program_total_blocks} blocks)...')

            # Send the program data to the serial port
            serial_port.write(program_data)
            serial_port.flush()

            # Now wait for 10 seconds (=cassette ramp-up time) + 2 times the number of blocks,
            # which allows the P2000T to save the received program to cassette tape
            sleep_seconds = 10 + 2 * program_total_blocks
            print(f'Waiting for {sleep_seconds} seconds while P2000T saves to cassette...')
            time.sleep(sleep_seconds)

if __name__ == '__main__':
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_port", help="Serial port to send the .cas file(s) to. E.g. COM4 (for Windows) or /dev/ttyUSB3 (for Linux and macOS)")
    parser.add_argument("cas_file_path", nargs='+', help="Path(s) to the .cas file(s)")
    
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

        # Call the function to send each .cas file to the serial port
        for cas_file in args.cas_file_path:
            send_cas_to_serial(cas_file, serial_port)
        print('Done!')

    finally:
        if serial_port.is_open:
            serial_port.close()