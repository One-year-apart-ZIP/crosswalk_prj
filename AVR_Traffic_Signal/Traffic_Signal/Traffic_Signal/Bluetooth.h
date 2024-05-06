/*
 * Bluetooth.h
 *
 * Created: 2024-05-06 오후 2:08:31
 *  Author: HoJoon
 */ 


#ifndef BLUETOOTH_H_
#define BLUETOOTH_H_

#include <avr/interrupt.h>

extern volatile unsigned char BLUETOOTH_RX_FLAG;
extern volatile char BLUETOOTH_RX_DATA;

ISR(USART1_RX_vect);

void Bluetooth_init(void);

#endif /* BLUETOOTH_H_ */