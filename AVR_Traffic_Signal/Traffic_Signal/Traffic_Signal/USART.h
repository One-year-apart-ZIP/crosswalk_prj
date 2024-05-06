/*
 * USART.h
 *
 * Created: 2024-05-01 오후 10:12:26
 *  Author: HoJoon
 */ 

#ifndef USART_H_
#define USART_H_

#define TXEN		(1 << TXEN0)
#define RXEN		(1 << RXEN0)

#define RXCIE		(1 << RXCIE0)
#define TXCIE		(1 << TXCIE0)
#define UDRIE		(1 << UDRIE0)

void USART1_init(void);
void USART1_transmit(char data);
void USART1_print_string(char* str);

#endif /* USART_H_ */