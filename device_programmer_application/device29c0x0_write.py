"""
Created on Sep 16, 2014

@author: sfurman
"""

import time

from progressbar import Bar, ETA, FileTransferSpeed, Percentage, ProgressBar, \
    RotatingMarker


# EEPROM write.
def device_29c0x0_write(ser, bin_str, color):
    widgets = [
        'Writing EEPROM: ',
        Percentage(), ' ',
        Bar(marker=RotatingMarker()),
        ' ', ETA(), ' ', FileTransferSpeed()]

    # Initiate WRITE sequence.
    ser.write('WRITE;')
    time.sleep(0.1)
    while ser.inWaiting() == 0:
        pass
    in_buffer = ''
    while ser.inWaiting() > 0:
        in_buffer += ser.read(1)
    print('Start writing sequence...')
    if in_buffer == 'START':
        print('OK.')
    else:
        print(
            color.TEXT_RED + 'Start writing sequence - error.' +
            color.TEXT_GREEN)
        print(in_buffer + '\n')

    bin_str_file_length = len(bin_str)
    print('Programming file length: %s bytes.\n' % bin_str_file_length)

    print(color.TEXT_CYAN + color.TEXT_BRIGHT)
    pbar = ProgressBar(widgets=widgets, maxval=bin_str_file_length).start()

    i = 0
    # Start writing data into EEPROM.
    for byte_to_write in bin_str:
        ser.write(byte_to_write)
        time.sleep(0.015)
        i = i + 1
        pbar.update(i)
    pbar.finish()
    print(color.TEXT_GREEN)
    # Wait until firmware sends END response.
    # (after firmware timed out in_buffer ~2 sec.).
    while ser.inWaiting() == 0:
        pass
    in_buffer = ''
    while ser.inWaiting() > 0:
        in_buffer += ser.read(1)
    print('End writing sequence...')
    if in_buffer == 'END':
        print('OK.\n')
    else:
        print(
            color.TEXT_RED + 'End writing sequence - error.' + color.TEXT_GREEN)
        print(in_buffer + '\n')

    return bin_str_file_length
