"""
Created on Aug 31, 2014

@author: sfurman
"""

import serial.tools.list_ports


# Find devices on the device list.
def com_port_devices():
    #  Search for ports using a regular expression. Port name, description and hardware ID.
    # [('COM3', 'USB Serial Port (COM3)', 'FTDIBUS\\COMPORT&VID_0403&PID_6001')]

    return list(serial.tools.list_ports.comports())
