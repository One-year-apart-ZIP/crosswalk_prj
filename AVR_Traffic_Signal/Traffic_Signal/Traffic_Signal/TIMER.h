/*
 * TIMER.h
 *
 * Created: 2024-05-06 오후 1:02:34
 *  Author: HoJoon
 */ 

#ifndef TIMER_H_
#define TIMER_H_

#include <avr/io.h>
#include <avr/interrupt.h>

#define OCR1		62499		//	PRE-SCALER 256

#define TIMER_CTC_MODE	(1 << WGM12)

#define TIMER_PRESCALER_1		(1 << CS10)
#define TIMER_PRESCALER_8		(1 << CS11)
#define TIMER_PRESCALER_64		(1 << CS11) | (1 << CS10)
#define TIMER_PRESCALER_256		(1 << CS12)
#define TIMER_PRESCALER_1024	(1 << CS12) | (1 << CS10)

extern volatile uint8_t TIMER1_COMPA_INT_FLAG;
extern volatile uint8_t wait_time;
volatile uint8_t timer_count;

ISR(TIMER1_COMPA_vect);

void TIMER1_COMPA_init(void);
void TIMER1_COMPA_clear(void);

#endif /* TIMER_H_ */