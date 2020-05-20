"""
Created on Aug 31, 2014

@author: sfurman
"""

import serial


# Set host serial device parameters and list available devices.
def set_serial(com_port):
    s = serial.Serial()
    s.port = com_port
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
