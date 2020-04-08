/*
 * File:   eeprom_funcs.c
 * Author: srdjan.furman
 *
 * Created on June 8, 2017, 9:42 AM
 */


/*
 * HARDWARE DATA PROTECTION
 * 
 * SOFTWARE DATA PROTECTION
 * 
 * ADDRESS

    How the address is create.
     xxxxxxxx xx111111   (PORTA)
            |
     xxxxxxxx 1xxxxxxx   (RC3)
            |
     xxxxxxxx x1xxxxxx   (RC2)
            |
     11111111 xxxxxxxx   (PORTB)
            |
  x1 xxxxxxxx xxxxxxxx   (RC0)
            |
  1x xxxxxxxx xxxxxxxx   (RC1)
            |
 1xx xxxxxxxx xxxxxxxx   (RC4)
            =
 111 11111111 11111111   (19-bit address)

 */


#include <xc.h>
#include "init_mcu.h"
#include "uart_funcs.h"
#include "eeprom_funcs.h"
#include "utility_funcs.h"


// EEPROM unlock (enable write).
// Write the special six-byte code to turn off Software Data Protection.
void EEPROM_unlock(void) {
    EEPROM_write(0xaa, 0x5555);
    EEPROM_write(0x55, 0x2aaa);
    EEPROM_write(0x80, 0x5555);
    EEPROM_write(0xaa, 0x5555);
    EEPROM_write(0x55, 0x2aaa);
    EEPROM_write(0x20, 0x5555);
}


// Initial EEPROM state.
void EEPROM_initial_state() {
    PORTEbits.RE2 = 1; // WE
    PORTEbits.RE0 = 1; // CE
    PORTEbits.RE1 = 1; // OE
}


// Read one byte from address.
unsigned char EEPROM_read(unsigned long address) {
    
    unsigned char data = 0;
    
    // Addresses within one page 6-bit (0-63).
    PORTA = (unsigned char)(address & 0x3f);            // xx11 1111
    // Page addresses 9-bit:
    // 64, 128, 192, 256, ... 32704 (01111111 11000000).
    PORTCbits.RC2 = ((address >> 6) & 0x01);            // x1xx xxxx
    PORTCbits.RC3 = ((address >> 7) & 0x01);            // 1xxx xxxx
    PORTB = (unsigned char)(((address) >> 8) & 0xff);   // 1111 1111 xxxx xxxx
    PORTCbits.RC0 = ((address >> 16) & 0x01);           // x1 xxxx xxxx xxxx xxxx
    PORTCbits.RC1 = ((address >> 17) & 0x01);           // 1x xxxx xxxx xxxx xxxx
    PORTCbits.RC4 = ((address >> 18) & 0x01);           // 1xx xxxx xxxx xxxx xxxx
    
    PORTEbits.RE0 = 0; // CE
    PORTEbits.RE1 = 0; // OE
    asm("nop");
    data = PORTD;
    PORTEbits.RE0 = 1; // CE
    PORTEbits.RE1 = 1; // OE

    return data;
}


// Write one byte on address.
void EEPROM_write(unsigned char data, unsigned long address) {
    
    PORTA = (unsigned char)(address & 0x3f);            // 0011 1111
    PORTCbits.RC2 = ((address >> 6) & 0x01);
    PORTCbits.RC3 = ((address >> 7) & 0x01);
    PORTB = (unsigned char)(((address) >> 8) & 0xff);
    PORTCbits.RC0 = ((address >> 16) & 0x01);           // x1 xxxx xxxx xxxx xxxx
    PORTCbits.RC1 = ((address >> 17) & 0x01);           // 1x xxxx xxxx xxxx xxxx
    PORTCbits.RC4 = ((address >> 18) & 0x01);           // 1xx xxxx xxxx xxxx xxxx
    PORTD = data;
    
    PORTEbits.RE0 = 0; // CE
    PORTEbits.RE2 = 0; // WE
    asm("nop");
    PORTEbits.RE0 = 1; // CE
    PORTEbits.RE2 = 1; // WE
}
