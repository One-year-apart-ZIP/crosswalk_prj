/*
 * TIMER.c
 *
 * Created: 2024-05-06 오후 1:03:44
 *  Author: HoJoon
 */ 

#include "TIMER.h"

volatile uint8_t TIMER1_COMPA_INT_FLAG = 0;
volatile uint8_t timer_count = 0;
volatile uint8_t wait_time = 10;

ISR(TIMER1_COMPA_vect)
{
	cli();
	timer_count++;
	
	if(timer_count >= wait_time)
	{
		TIMER1_COMPA_INT_FLAG = 1;
		timer_count = 0;
	}
	
	TCNT1 = 0;
	sei();
}

void TIMER1_COMPA_init(void)
{
	timer_count = 0;
	TIMSK |= (1 << OCIE1A);
	TCCR1B |= TIMER_CTC_MODE;
	OCR1A = OCR1;
	TCCR1B |= TIMER_PRESCALER_256;
}

void TIMER1_COMPA_clear(void)
{
	TIMSK &= ~(1 << OCIE1A);
	TCCR1B = 0x00;
	OCR1A = 0;
}