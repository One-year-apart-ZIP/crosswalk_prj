/*
 * Bluetooth.c
 *
 * Created: 2024-05-06 오후 2:31:05
 *  Author: HoJoon
 */ 

#define F_CPU 16000000L

#include "Bluetooth.h"
#include "USART.h"

#include <util/delay.h>

volatile unsigned char BLUETOOTH_RX_FLAG = 0;
volatile char BLUETOOTH_RX_DATA = 0;

ISR(USART1_RX_vect)
{
	cli();
	BLUETOOTH_RX_FLAG = 1;
	BLUETOOTH_RX_DATA = UDR1;
	sei();
}

void Bluetooth_init()
{
	USART1_init();

	_delay_ms(500);
	
	USART1_print_string("AT");
	_delay_ms(1000);
	USART1_print_string("AT+NAMEBlueTmega128");
	_delay_ms(1000);
	// UART1_print_string("AT+PIN1234");
	// _delay_ms(1000);
	USART1_print_string("AT+BAUD4");
	_delay_ms(1000);
}