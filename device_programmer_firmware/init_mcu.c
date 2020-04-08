/*
 * File:   init_mcu.c
 * Author: srdjan.furman
 *
 * Created on June 8, 2017, 9:40 AM
 */


#include <xc.h>


// MCU init.
void init_mcu(void) {
    // Turn off all interrupts.
    INTCON = 0x00;

    // PORTA
    // A0 - A5. Addresses digital. (initially set as output low).
    // A7 and A6 are OSC1 and OSC2.
    ADCON1 = 0x0f;
    
    TRISAbits.RA0 = 0;
    TRISAbits.RA1 = 0;
    TRISAbits.RA2 = 0;
    TRISAbits.RA3 = 0;
    TRISAbits.RA4 = 0;
    TRISAbits.RA5 = 0;
    PORTAbits.RA0 = 0;
    PORTAbits.RA1 = 0;
    PORTAbits.RA2 = 0;
    PORTAbits.RA3 = 0;
    PORTAbits.RA4 = 0;
    PORTAbits.RA5 = 0;

    // PORTB
    // A8 - A15. (initially set as output low).
    TRISB = 0x00;
    PORTB = 0x00;

    // PORTC
    // A16, A17, A6, A7, A18. (initially set as output low).
    TRISCbits.RC0 = 0;
    TRISCbits.RC1 = 0;
    TRISCbits.RC2 = 0;
    TRISCbits.RC3 = 0;
    TRISCbits.RC4 = 0;
    
    PORTCbits.RC0 = 0;
    PORTCbits.RC1 = 0;
    PORTCbits.RC2 = 0;
    PORTCbits.RC3 = 0;
    PORTCbits.RC4 = 0;
    
    // PORTD
    // I/O data port. (initially set as input - no pull-ups).
    TRISD = 0xff;

    // PORTE
    // Control pins. (initially set as output high).
    TRISEbits.RE0 = 0;
    TRISEbits.RE1 = 0;
    TRISEbits.RE2 = 0;
    PORTEbits.RE0 = 1;  // CE
    PORTEbits.RE1 = 1;  // OE
    PORTEbits.RE2 = 1;  // WE
}
