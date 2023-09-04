#ifndef UARTSEND_H
#define UARTSEND_H

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "header/prioritylist.h"
#include <string.h>

#define UART_QUENE_BUFFER_SIZE  50

extern QueueHandle_t tx_quene_A;
void UARTS_write(char* data);

#endif