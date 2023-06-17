#ifndef COMMANDDISTRIBUTE_H
#define COMMANDDISTRIBUTE_H

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include <string.h>
#include "UartSend.h"
#include "SystemHandle.h"
#include "stdlib.h"
#include "header/commandlist.h"
#include "header/prioritylist.h"
#include "CurveHandle.h"
#include "ApproachHandle.h"
#include "CurveTestHandle.h"
#include "ScanHandle.h"


#define COMMAND_LENGTH  5
#define DATA_LENGTH     5


extern QueueHandle_t system_handle_quene;
extern QueueHandle_t curve_handle_queue;
extern QueueHandle_t approach_handle_queue;
extern QueueHandle_t curve_test_handle_queue;
extern QueueHandle_t scan_handle_queue;

extern TaskHandle_t approach_handle;
extern TaskHandle_t system_handle;
extern TaskHandle_t curve_handle;
extern TaskHandle_t curve_test_handle;
extern TaskHandle_t scan_handle;


void commandD_init();
void commandD_task(void *arg);

#endif

