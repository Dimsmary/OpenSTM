#ifndef APPROACHHANDLECONTROL_H
#define APPROACHHANDLECONTROL_H

#include "header/commandlist.h"
#include "header/prioritylist.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "UartSend.h"
#include "hardware/adda.h"
#include "command/cformat.h"
#include "rom/ets_sys.h"

void approach_status_switch(int sta);
extern QueueHandle_t approach_handle_queue;


#endif