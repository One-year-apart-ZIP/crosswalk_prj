/*
 * LED.h
 *
 * Created: 2024-05-06 오전 11:42:25
 *  Author: HoJoon
 */ 


#ifndef LED_H_
#define LED_H_

#include <avr/io.h>

#define GREEN_LED		PORTC2
#define RED_LED			PORTC0

#define AVAILABLE	1
#define UNAVAILABLE	0

extern unsigned char increase_available;

#define TOGGLE_LED()		(PORTC ^= (1 << GREEN_LED) | (1 << RED_LED))
#define IS_GREEN_LIGHT()	(PORTC & (1 << GREEN_LED))

void LED_init(void);
void LED_toggle(void);

#endif /* LED_H_ */