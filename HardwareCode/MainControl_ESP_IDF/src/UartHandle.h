// Ref:https://github.com/espressif/esp-idf/blob/49551cc48cb3cdd5563059028749616de313f0ec/examples/peripherals/uart/uart_async_rxtxtasks/main/uart_async_rxtxtasks_main.c
#ifndef uarthandle_h
#define uarthandle_h

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_system.h"
#include "esp_log.h"
#include "driver/uart.h"
#include <string.h>
#include "driver/gpio.h"
#include "CommandDistribute.h"
#include "header/prioritylist.h"


#define TXD_PIN         1
#define RXD_PIN         3
#define RX_BUF_SIZE     1024
#define UART UART_NUM_0

#define FAST_BAUD_RATE

#ifndef FAST_BAUD_RATE
#define BAUD_RATE       115200
#else
#define BAUD_RATE       1200000
#endif

extern QueueHandle_t command_distribute_quene;
void uarth_init();
void uarth_tx_task(void *arg);
void uarth_rx_task(void *arg);

#endif