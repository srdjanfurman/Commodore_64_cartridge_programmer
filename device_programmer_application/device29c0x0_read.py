"""
Created on Sep 16, 2014

@author: sfurman
"""

import time

from progressbar import Bar, ETA, FileTransferSpeed, Percentage, ProgressBar, \
    RotatingMarker

from twos_complement_checksum import twos_complement_chksum


# EEPROM read.
def device_29c0x0_read(ser, max_num_of_bytes_read, color):
    widgets = [
        'Reading EEPROM: ',
        Percentage(), ' ',
        Bar(marker=RotatingMarker()),
        ' ', ETA(), ' ', FileTransferSpeed()]

    # Initiate READ sequence.
    ser.write('READ;')
    time.sleep(0.1)
    while ser.inWaiting() == 0:
        pass
    in_buffer = ''
    while ser.inWaiting() > 0:
        in_buffer += ser.read(1)
    print('\nStart reading sequence...')
    if in_buffer == 'START':
        print('OK.')
    else:
        print(color.TEXT_RED + 'Start reading sequence - error.'
              + color.TEXT_GREEN)
        print(in_buffer + '\n')

    max_num_of_bytes_read_str = '%s;' % max_num_of_bytes_read

    # Initiate a number of bytes to be read (max address) -
    # (for example: 5931;).
    ser.write(max_num_of_bytes_read_str)
    time.sleep(0.1)
    while ser.inWaiting() == 0:
        pass
    in_buffer = ''
    while ser.inWaiting() > 0:
        in_buffer += ser.read(1)
    print('\nThe number of bytes to be read accepted...')
    if in_buffer == 'DONE':
        print('OK.')
    else:
        print(color.TEXT_RED +
              'Bytes-to-be-read receiving - error.' + color.TEXT_GREEN)
        print(in_buffer + '\n')

    # in_buffer = ''
    read_data_string = ''
    num_of_bytes_read = 0
    print(color.TEXT_CYAN + color.TEXT_BRIGHT)
    # maxval=max_num_of_bytes_read tested! :)
    pbar = ProgressBar(widgets=widgets, maxval=max_num_of_bytes_read).start()

    # Start reading data from EEPROM.
    while num_of_bytes_read < max_num_of_bytes_read:
        while ser.inWaiting() > 0:
            read_data_string += ser.read(1)
            #                     time.sleep(0.01)
            num_of_bytes_read += 1
            pbar.update(num_of_bytes_read)
    pbar.finish()
    print('%s' % num_of_bytes_read)
    print(color.TEXT_GREEN)

    memory_chksum = twos_complement_chksum(read_data_string)

    return memory_chksum
