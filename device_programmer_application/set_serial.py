"""
Created on Aug 31, 2014

@author: sfurman
"""

import serial

from device_list_and_select import device_list_and_select


# Set host serial device parameters and list available devices.
def set_serial():
    s = serial.Serial()
    s.port = 'COM' + device_list_and_select()
    s.baudrate = 19200  # 115200
    s.bytesize = serial.EIGHTBITS
    s.parity = serial.PARITY_NONE
    s.stopbits = serial.STOPBITS_ONE
    s.timeout = None  # Read or write the current read timeout setting.
    s.xonxoff = False
    s.rtscts = False
    s.dsrdtr = False
    s.writeTimeout = None  # Read or write the current write timeout setting.
    return s


'''
timeout = None: wait forever
timeout = 0: non-blocking mode (return immediately on read)
timeout = x: set timeout to x seconds (float allowed)
'''
