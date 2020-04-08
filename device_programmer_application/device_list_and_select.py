"""
Created on Aug 31, 2014

@author: sfurman
"""

import sys
import time

import serial.tools.list_ports

from colors import Color


# Find devices on the device list.
def device_list_and_select():
    color = Color()
    # Device name under Windows OS Device manager.
    search_string_1 = 'Communication Device Class ASF example (COM'
    search_string_2 = 'USB Serial Port (COM'
    # search_string_3 = 'Communications Port (COM'
    # search_string_2 = 'Standard Serial over Bluetooth link (COM'

    full_list = list(serial.tools.list_ports.comports())

    # full_list_str = str(full_list)  # List to string conversion.

    total_devices = 0  # The number of available devices (2 max.).
    first_device_found = 0  # Flag - device found.
    second_device_found = 0
    first_device_port_digits = 0  # Flag - port number of digits (2 max.).
    second_device_port_digits = 0
    first_device_port_number = []  # A Port number contains more than one digit.
    second_device_port_number = []

    # First device search.
    for i in full_list:  # Iterate through every single element in a list.
        # Convert a single element from the list into a string.
        full_list_str = str(i)
        # In general, is the search_string_1 in a list?
        if search_string_1 in full_list_str:
            total_devices = total_devices + 1
            first_device_found = 1
            if full_list_str[
               full_list_str.find(search_string_1) + len(search_string_1):
                    full_list_str.find(search_string_1) + len(
                           search_string_1) + 1].isdigit():
                if full_list_str[
                   full_list_str.find(search_string_1) + len(search_string_1):
                        full_list_str.find(search_string_1) + len(
                               search_string_1) + 2].isdigit():
                    first_device_port_number += full_list_str[
                                                full_list_str.find(
                                                    search_string_1) + len(
                                                    search_string_1):
                                                full_list_str.find(
                                                    search_string_1) + len(
                                                    search_string_1) + 2]
                    first_device_port_digits = 2
                    print(str(total_devices) + '. ' + search_string_1 +
                          first_device_port_number[0] +
                          first_device_port_number[1] + ')')
                else:
                    first_device_port_number += full_list_str[
                                                full_list_str.find(
                                                    search_string_1) + len(
                                                    search_string_1):
                                                full_list_str.find(
                                                    search_string_1) + len(
                                                    search_string_1) + 1]
                    first_device_port_digits = 1
                    print(str(total_devices) + '. ' + search_string_1 +
                          first_device_port_number[0] + ')')
        if first_device_found:
            break

    # Second device search.
    for i in full_list:
        full_list_str = str(i)
        if search_string_2 in full_list_str:

            total_devices = total_devices + 1
            second_device_found = 1

            if full_list_str[
               full_list_str.find(search_string_2) + len(search_string_2):
                    full_list_str.find(search_string_2) + len(
                           search_string_2) + 1].isdigit():
                if full_list_str[
                   full_list_str.find(search_string_2) + len(search_string_2):
                        full_list_str.find(search_string_2) + len(
                               search_string_2) + 2].isdigit():
                    second_device_port_number += full_list_str[
                                                 full_list_str.find(
                                                     search_string_2) + len(
                                                     search_string_2):
                                                 full_list_str.find(
                                                     search_string_2) + len(
                                                     search_string_2) + 2]
                    second_device_port_digits = 2
                    print(str(total_devices) + '. ' + search_string_2 +
                          second_device_port_number[0] +
                          second_device_port_number[1] + ')')
                else:
                    second_device_port_number += full_list_str[
                                                 full_list_str.find(
                                                     search_string_2) + len(
                                                     search_string_2):
                                                 full_list_str.find(
                                                     search_string_2) + len(
                                                     search_string_2) + 1]
                    second_device_port_digits = 1
                    print(str(total_devices) + '. ' + search_string_2 +
                          second_device_port_number[0] + ')')
        if second_device_found:
            break

    if first_device_found == 0 and second_device_found == 0:
        print(
            color.TEXT_YELLOW + 'Target device not found.\n' + color.TEXT_GREEN)
        raw_input('Exit [enter]')
        time.sleep(0.5)
        sys.exit()

    # Device selection.
    print('\nSelect device number from the list:')
    while 1:
        while 1:
            try:
                # in_selection = 0
                # Robust error handling only accepts int.
                in_selection = int(raw_input('>> '))
            except Exception, e:
                print(color.TEXT_RED + '\nError: ' + str(e) + color.TEXT_GREEN)
                print('\r')
                break
            else:
                if total_devices == 1:
                    if in_selection == 1:
                        if first_device_found:
                            if first_device_port_digits == 2:
                                return first_device_port_number[0] + \
                                       first_device_port_number[1]
                            elif first_device_port_digits == 1:
                                return first_device_port_number[0]
                        if second_device_found:
                            if second_device_port_digits == 2:
                                return second_device_port_number[0] + \
                                       second_device_port_number[1]
                            elif second_device_port_digits == 1:
                                return second_device_port_number[0]
                    else:
                        print(color.TEXT_YELLOW +
                              'Wrong selection.\n' + color.TEXT_GREEN)

                if total_devices == 2:
                    if in_selection == 1:
                        if first_device_found:
                            if first_device_port_digits == 2:
                                return first_device_port_number[0] + \
                                       first_device_port_number[1]
                            elif first_device_port_digits == 1:
                                return first_device_port_number[0]
                    elif in_selection == 2:
                        if second_device_found:
                            if second_device_port_digits == 2:
                                return second_device_port_number[0] + \
                                       second_device_port_number[1]
                            elif second_device_port_digits == 1:
                                return second_device_port_number[0]
                    else:
                        print(color.TEXT_YELLOW +
                              'Wrong selection.\n' + color.TEXT_GREEN)
