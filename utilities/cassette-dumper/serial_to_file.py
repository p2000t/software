#
# serial_to_file.py 
#

import serial
import argparse

if __name__ == '__main__':
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_port", help="Serial I/O port connected to the P2000T. E.g. COM4 (for Windows) or /dev/ttyUSB3 (for Linux and macOS)")
    parser.add_argument("destination_file", help="Path to the destination .cas file")
    
    # Parse arguments
    args = parser.parse_args()
    block_counter = 0
    block_bytes = 0
    block = bytearray(1280)

    try:
        # Create serial port with the specified settings
        serial_port = serial.Serial(
            port=args.serial_port,
            baudrate=9600, 
            parity=serial.PARITY_NONE, 
            stopbits=serial.STOPBITS_ONE, 
            bytesize=serial.EIGHTBITS,
            timeout=1)

        with open(args.destination_file, 'wb') as file:
            print(f'Waiting for P2000T to send data... (press Ctrl+C to stop)')
            while True:
                byte = serial_port.read(1)
                if byte:
                    block[block_bytes] = byte
                    if block_bytes == 0:
                        block_counter += 1
                        print(f'Saving block {block_counter} to file...', end="", flush=True)
                    block_bytes += 1
                    if block_bytes == 1280:
                        file.write(block)
                        block_bytes = 0      
                        print("Done")
                        print("Waiting for more data... (press Ctrl+C to stop)")
    finally:
        if serial_port.is_open:
            serial_port.close()