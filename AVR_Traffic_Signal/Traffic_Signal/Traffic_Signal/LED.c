/*
 * LED.c
 *
 * Created: 2024-05-06 오전 11:46:24
 *  Author: HoJoon
 */ 

#include "LED.h"

unsigned char increase_available = AVAILABLE;

void LED_init(void)
{
	DDRC |= (1 << GREEN_LED) | (1 << RED_LED);
	PORTC &= ~((1 << GREEN_LED) | (1 << RED_LED));
}

void LED_toggle(void)
{
	TOGGLE_LED();
	increase_available = AVAILABLE;
}