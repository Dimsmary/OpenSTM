#ifndef SYSTEMHANDLE_H
#define SYSTEMHANDLE_H

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "UartSend.h"
#include "hardware/ad5761.h"
#include "hardware/adda.h"
#include "header/commandlist.h"
#include "header/prioritylist.h"


#define SYSTEM_VERSION_NOW      "\r\nVERSI=Test"


void systemH_task(void *arg);
void systemH_init();
void systemH_return_value(char *prefix, int value);

#endif