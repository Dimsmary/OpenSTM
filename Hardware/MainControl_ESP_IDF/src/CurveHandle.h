#ifndef CURVEHANDLE_H
#define CURVEHANDLE_H

#include "header/commandlist.h"
#include "header/prioritylist.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "UartSend.h"
#include "hardware/adda.h"
#include "command/cformat.h"

void curveH_init();
void curveH_task(void *arg);

#endif