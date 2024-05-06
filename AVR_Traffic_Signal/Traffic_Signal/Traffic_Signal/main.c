/*
* bluetooth_practice.c
*
* Created: 2024-05-01 오후 10:08:27
* Author : HoJoon
*/

#include <avr/io.h>

#include "Traffic_light.h"

void Interrupt_handler(void);

int main(void)
{
	LED_init();
	Bluetooth_init();
	
	PORTC |= (1 << RED_LED);
	
	TIMER1_COMPA_init();
	
	sei();
	
	while (1)
	{
		Interrupt_handler();
	}
	
	return 0;
}

void Interrupt_handler(void)
{
	// USART INTERRUPT HANDLER
	if (BLUETOOTH_RX_FLAG == 1)
	{
		BLUETOOTH_RX_FLAG = 0;
		if(BLUETOOTH_RX_DATA == 'S' && IS_GREEN_LIGHT() && increase_available == AVAILABLE)
		{
			wait_time += 5;
			increase_available = UNAVAILABLE;
		}
	}
	
	// TIMER1 COMPA INTERRUPT HANDLER
	if (TIMER1_COMPA_INT_FLAG == 1)
	{
		TIMER1_COMPA_INT_FLAG = 0;
		LED_toggle();
		wait_time = 10;
	}
}