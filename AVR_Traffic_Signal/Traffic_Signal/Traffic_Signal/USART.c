/*
* USART.c
*
* Created: 2024-05-01 오후 10:14:04
*  Author: HoJoon
*/

#include "USART.h"

#include <avr/io.h>

void USART1_init(void)
{
	UBRR1H = 0x00;
	UBRR1L = 207;
	
	UCSR1A |= (1 << U2X1);
	UCSR1C |= 0x06;
	
	UCSR1B |= RXEN | TXEN;
	UCSR1B |= RXCIE;
}

void USART1_transmit(char data)
{
	while(!(UCSR1A & (1 << UDRE1)));
	UDR1 = data;
}

void USART1_print_string(char* str)
{
	for(int i = 0; str[i]; ++i)
	{
		USART1_transmit(str[i]);
	}
}