/*
 * File:   main.c
 * Author: srdjan.furman
 *
 * Compiler: XC8 (v1.41)
 * IDE: MPLAB X IDE v3.50
 *
 * Created on June 8, 2017, 9:41 AM
 */


#include <xc.h>
#include <string.h>
#include <stdlib.h>
#include "uart_funcs.h"
#include "init_mcu.h"
#include "eeprom_funcs.h"
#include "utility_funcs.h"


const unsigned char
version_response[] = {"v1.0"},
start_response[] = {"START"},
end_response[] = {"END"},
done_response[] = {"DONE"},
        
unknown_message[] = {"\n\r UNKNOWN \n\r"},
test_message[] = {"\n\r TEST MODE \n\r"},
start_message[] = {"\n\r START \n\r"},
end_message[] = {"\n\r END \n\r"};

// Main.
void main(void) {
    init_mcu();
    UART_Init(19200);
    __delay_ms(500);
    
    // Prerequisites for write operation.
    MCU_data_line_write();
    // Unlock EEPROM for any case.
    EEPROM_unlock();

    unsigned char* command = NULL;
    unsigned char* max_num_of_bytes_read = NULL;
    
    unsigned int sector_idx;
    unsigned char sector_mod_idx;
    
    unsigned char end_flag;
    unsigned char data_byte;
    unsigned char data_byte_array[256];
    unsigned char received_term_data;
    
    unsigned long address;
    unsigned long max_address;
    
//    unsigned int data_byte_16;
    unsigned long timeout;
    
    unsigned char test_chr = 0;
    const unsigned int sector_full_address = 256;
    

    for (;;) {
        
        // Commands loop.
        received_term_data = 0;
        
        for (;;) {
            command = UART_Read_Command();

            // Version.
            if (strcmp(command, "VERSION") == 0) {
                UART_Write_Const(version_response);
            }

            
            // Write to EEPROM.
            else if (strcmp(command, "WRITE") == 0) {
                UART_Write_Const(start_response); // Send START to APP to start to WRITE data byte stream.

                timeout = 0;
                end_flag = 0;
                address = 0;
                data_byte = 0;
                sector_mod_idx = 0;
                
                // Prerequisites for the write operation.
                MCU_data_line_write();

                for (;;) {
                    // Set end_flag if byte sending is finished - timeout overflow.
                    while (UART_Data_Ready() == 0) {
                        timeout++;
                        if (timeout >= MAX_TIMEOUT) { // APP stopped sending data - all data sent.
                            end_flag = 1;
                            break;
                        }
                    }
                    timeout = 0;
                    
                    sector_mod_idx = address % 256; // sector_mod_idx: 0-255
                    
                    // Check if byte sending is finished. If so, don't wait for the new byte - don't block.
                    if (end_flag == 0) {
                        data_byte = UART_Read();
                    }
                    
                    // Program EEPROM with the last 256 bytes received.
                    if (sector_mod_idx == 0 && address != 0) {
                        address -= sector_full_address;
                        for (sector_idx = 0; sector_idx < sector_full_address; sector_idx++) {
                            // At this point:
                            // sector_idx = 0-255.
                            // address: 0-255, 256-511, 512-767, 768-1023, 1024-1279,...
                            EEPROM_write(data_byte_array[sector_idx], address);
                            address++;
                        }
                        // At this point, sector_idx = 256 always and address = 256, 512, 768, 1024,...
                        __delay_ms(10); // Write Cycle Time = 10ms max.
                    }
                    
                    // Check again if byte sending is finished. If so, send end_response and break.
                    if (end_flag == 1) {
                        // Program extra sector_mod_idx bytes after the last EEPROM write.
                        address -= sector_mod_idx;
                        for (sector_idx = 0; sector_idx < sector_mod_idx; sector_idx++) {
                            EEPROM_write(data_byte_array[sector_idx], address);
                            address++;
                        }
                        UART_Write_Const(end_response); // Send END to APP to exit writing cycle.
                        break;
                    }
                    
                    // Put last received byte into an array of 256 bytes and increment address.
                    data_byte_array[sector_mod_idx] = data_byte; // [0-255]
                    address++;
                }
                EEPROM_initial_state();
            }

            
            // Read from EEPROM.
            else if (strcmp(command, "READ") == 0) {
                UART_Write_Const(start_response); // Send START to APP to start to READ data byte stream.

                max_address = 0;
                data_byte = 0;
                
                max_num_of_bytes_read = UART_Read_Command();
                max_address = atol(max_num_of_bytes_read);
                UART_Write_Const(done_response);
                __delay_ms(100);
                
                // Prerequisites for read operation.
                EEPROM_initial_state();
                MCU_data_line_read();
                
                for (address = 0; address < max_address; address++) {
                    data_byte = EEPROM_read(address);
                    UART_Write(data_byte);
                }
            }

            
            // Switch into test mode.
            else if (strcmp(command, "TEST") == 0) {
                UART_Write_Const(test_message);
                break;
            }
            
            
            // Unknown command.
            else {
                UART_Write_Const(unknown_message);
            }
        }

        
        // Tests loop.
        for (;;) {
            while (UART_Data_Ready() == 0) {
                asm("nop");
            }
            received_term_data = UART_Read();

            // Test get_address() function.
            if (received_term_data == 't') {
                UART_Write_Const(start_message);

                for (address = 0; address < CYCLES; address++) {
                    print_address(address);
                    UART_Write(CR);
                    UART_Write(LF);
                }
                UART_Write_Const(end_message);
            }


            // Read data bytes.
            if (received_term_data == 'r') {
                UART_Write_Const(start_message);
                
                data_byte = 0;
                
                // Prerequisites for read operation.
                EEPROM_initial_state();
                MCU_data_line_read();
                
                for (address = 0; address < CYCLES; address++) {
//                    print_long_address(address);
                    data_byte = EEPROM_read(address);
                    print_long_address(address);
                    UART_Write_Const("   ");
                    print_char(data_byte);
                    UART_Write(CR);
                    UART_Write(LF);
                }
//                print_address(address);
                UART_Write_Const(end_message);
            }


            // Write data bytes.
            if (received_term_data == 'w') {
                UART_Write_Const(start_message);
                
                test_chr = '1';
                
                // Prerequisites for write operation.
                MCU_data_line_write();
                
                for (address = 0; address < CYCLES; address++) {
                    
                    if (address == 500) {
                        test_chr = '0';
                    }
                    
                    if (address % 256 == 0 && address != 0) {
                        __delay_ms(10);
                    }
                    EEPROM_write(test_chr, address);
                }
                __delay_ms(10);
                
                EEPROM_initial_state();
                
//                print_address(address);
                UART_Write_Const(end_message);
            }
            break;
        }
    }
}
