/*
 * File:   uart_funcs.c
 * Author: srdjan.furman
 *
 * Created on June 8, 2017, 9:45 AM
 */


#include <xc.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include "init_mcu.h"
#include "uart_funcs.h"


// UART initialize.
unsigned char UART_Init(const long int baudrate) {
    unsigned int x;
    x = (_XTAL_FREQ - baudrate*64) / (baudrate*64);   // SPBRG for low baud rate.

    if (x > 255) { // If the high baud rate required...
        x = (_XTAL_FREQ - baudrate*16)/(baudrate*16); // SPBRG for high baud rate.
        BRGH = 1;                                     // Setting for high baud rate.
    }

    if (x < 256) {
        SPBRG = x;      // Writing SPBRG register.
        SYNC = 0;       // Setting asynchronous mode, i.e. UART.
        SPEN = 1;       // Enables serial port.
        TRISC7 = 1;     // As prescribed in the datasheet.
        TRISC6 = 1;     // As prescribed in the datasheet.
        CREN = 1;       // Enables continuous reception.
        TXEN = 1;       // Enables transmission.
        return 0;       // Returns 0 to indicate successful completion.
    }
    return 1;           // Returns 1 to indicate UART initialization failed.
}


// Data received or not.
unsigned char UART_Data_Ready() {
    return RCIF;
}


// Read a character.
unsigned char UART_Read() {
    while (!RCIF);
    return RCREG;
}


// Write a character.
void UART_Write(unsigned char data) {
    while (!TRMT);
    TXREG = data;
}


void UART_Write_Const(const unsigned char *s) {
    while (*s) {
        UART_Write(*s);
        s++;
    }
}


void UART_Write_Var(unsigned char *s) {
    while (*s) {
        UART_Write(*s);
        s++;
    }
}


// Receive string from UART.
unsigned char* UART_Read_Command() {
    unsigned char i;
    unsigned char received_char = 0;
    static unsigned char received_string[10];

    for (i=0; i<10; i++) {
        while (UART_Data_Ready() == 0) {
            asm("nop");
            // timeout
        }
        received_char = UART_Read();
        if (received_char == ';') {
            break; // Do not write semicolon into return string.
        }
        received_string[i] = received_char;
    }
    received_string[i] = '\0'; // Terminate string.
    return received_string;
}
