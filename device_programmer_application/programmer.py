"""
Created on Sep 16, 2014

@author: sfurman
"""

import sys
import time

from colorama import init

from colors import Color
from device29c0x0_read import device_29c0x0_read
from device29c0x0_write import device_29c0x0_write
from com_port_devices import com_port_devices
from set_serial import set_serial
from twos_complement_checksum import twos_complement_chksum

init()


# Main function.
def main(binary_file):
    color = Color()

    print(color.TEXT_RESET_ALL)
    print(color.TEXT_BRIGHT)

    header1 = '=======================================\n'
    header2 = '---- 29C020(040) programmer v1.0.0 ----\n'
    header3 = '======================================='
    print(color.TEXT_GREEN + header1 + header2 + header3)

    while 1:
        while 1:
            print('** Choose operation **')
            print('p - Program device')
            print('q - Quit program')

            try:
                operation_selection = raw_input('>> ')
            except Exception, e:  # Don't exit - warn.
                print(color.TEXT_RED + '\nError: ' + str(e) + color.TEXT_GREEN)
                print('\r')
                break
            else:
                if operation_selection == 'p':

                    print('\n** Select target device number from the list **')
                    com_port_devices_list = com_port_devices()

                    idx = 0
                    devices = dict()

                    for com_port_device in com_port_devices_list:
                        idx += 1
                        devices[idx] = com_port_device[0]
                        print('{0}. {1}'.format(idx, com_port_device[1]))

                    try:
                        device_selection = int(raw_input('>> '))
                    except Exception, e:
                        print(color.TEXT_YELLOW + 'Target device not found. ({})\n'.format(e) + color.TEXT_GREEN)
                        break
                    else:
                        if device_selection in devices.keys():
                            com_port = devices[device_selection]
                        else:
                            print(color.TEXT_YELLOW + 'Wrong selection.\n' + color.TEXT_GREEN)
                            break

                    ser = set_serial(com_port)

                    try:
                        ser.open()
                        # Flush input buffer discarding all it's contents.
                        # Clear output buffer aborting the current output and
                        # discarding all in the buffer.
                        ser.flushInput()
                        ser.flushOutput()
                    except Exception, e:  # Port already opened (port in use).
                        print(color.TEXT_RED + 'Error opening serial port: {}\n'.format(str(e)) + color.TEXT_GREEN)
                        print('\r')
                        break  # Don't exit - warn.

                    # Get the firmware version.
                    ser.write('VERSION;')
                    time.sleep(0.1)
                    while ser.inWaiting() == 0:
                        pass
                    in_buffer = ''
                    while ser.inWaiting() > 0:
                        in_buffer += ser.read(1)
                    print('FW version %s.' % in_buffer)

                    # Read the binary file from a specified location.
                    bin_file = open(binary_file, 'rb')
                    bin_str = bin_file.read()

                    # Calculate Two's Complement checksum for the binary file
                    # before writing it's content into EEPROM.
                    original_chksum = twos_complement_chksum(bin_str)
                    print('%s device selected.\n' % ser.portstr)
                    print('Loaded input file: %s.' % bin_file)

                    # Program device.
                    print(color.TEXT_MAGENTA + 'Program device.\n' + color.TEXT_GREEN)
                    bin_str_file_length = device_29c0x0_write(ser, bin_str, color)

                    # Verify device.
                    print(color.TEXT_MAGENTA + 'Verify device.\n' + color.TEXT_GREEN)
                    calculated_checksum = device_29c0x0_read(ser, bin_str_file_length, color)

                    # Match program checksums.
                    if calculated_checksum == original_chksum:
                        print('VERIFIED.\n')
                    else:
                        print('CHECKSUM ERROR.\n')

                    ser.close()

                elif operation_selection == 'q':
                    print(color.TEXT_WHITE + 'Thank you for using the 29C020(040) programmer.' + color.TEXT_RESET_ALL)
                    time.sleep(0.2)
                    sys.exit()
                else:
                    print(color.TEXT_YELLOW + 'Wrong selection.\n' + color.TEXT_GREEN)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python programmer.py <filename.bin>')
        sys.exit()
    else:
        main(sys.argv[1])
        sys.exit()
