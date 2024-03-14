#
# rom_to_file.py 
#
# note: this requires the libaries 'pyserial' and 'keyboard' to be installed:
#   pip install pyserial, keyboard
#

import serial
import keyboard
import argparse

if __name__ == '__main__':
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("serial_port", help="Serial I/O port connected to the P2000T. E.g. COM4 (for Windows) or /dev/ttyUSB3 (for Linux and macOS)")
    parser.add_argument("destination_file", help="Path to the destination .bin file")
    
    # Parse arguments
    args = parser.parse_args()
    block_counter = 0
    block_bytes = 0
    block = bytearray(1024)

    try:
        # Create serial port with the specified settings
        serial_port = serial.Serial(
            port=args.serial_port,
            baudrate=9600, 
            parity=serial.PARITY_NONE, 
            stopbits=serial.STOPBITS_ONE, 
            bytesize=serial.EIGHTBITS,
            timeout=0)

        with open(args.destination_file, 'wb') as file:
            print(f'Waiting for P2000T to send ROM data... (press Esc to stop)')
            while True:
                if keyboard.is_pressed("esc"):
                    print("Stopped")
                    break
                byte = serial_port.read(1)
                if byte:
                    block[block_bytes] = byte[0]
                    if block_counter == 0:
                        print(f'Saving ROM bytes to file...', flush=True)
                    if block_bytes == 0:
                        block_counter += 1
                    block_bytes += 1
                    if block_bytes == 1024:
                        file.write(block)
                        block_bytes = 0      
    finally:
        if serial_port.is_open:
            serial_port.close()
