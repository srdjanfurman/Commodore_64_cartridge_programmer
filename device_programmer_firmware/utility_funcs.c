/*
 * File:   utility_funcs.c
 * Author: srdjan.furman
 *
 * Created on June 8, 2017, 9:39 AM
 */


#include <xc.h>
#include <stdio.h>
#include "init_mcu.h"
#include "uart_funcs.h"

extern unsigned int addressHi;

// PORTD (data I/O) all pins input.
void MCU_data_line_read() {
    TRISD = 0xff;
    __delay_ms(1);
}


// PORTD (data I/O) all pins output.
void MCU_data_line_write() {
    TRISD = 0x00;
    __delay_ms(1);
}


// Print char on Terminal.
void print_char(unsigned char data_to_print) {
    unsigned char byte_data_str[1];
    sprintf(byte_data_str, "%c", data_to_print);
    UART_Write_Const("Char: ");
    UART_Write_Var(byte_data_str);
}


// Print address int on Terminal.
void print_address(unsigned int data_to_print) {
    unsigned char int_data_str[7];
    sprintf(int_data_str, "%u", data_to_print);
    UART_Write_Const("Address: ");
    UART_Write_Var(int_data_str);
}


// Print address long on Terminal.
void print_long_address(unsigned long data_to_print) {
    unsigned char long_data_str[15];
    sprintf(long_data_str, "%lu", data_to_print);
    UART_Write_Const("Long address: ");
    UART_Write_Var(long_data_str);
}
