#ifndef SCANHANDLE_H
#define SCANHANDLE_H

#include "header/commandlist.h"
#include "header/prioritylist.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "UartSend.h"
#include "hardware/adda.h"
#include "command/cformat.h"
#include "rom/ets_sys.h"
#include "ApproachHandleControl.h"
#include "header/da_order.h"
#include "esp_timer.h"

void scanH_init();
void scanH_task(void *arg);

#endif