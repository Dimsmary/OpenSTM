#include "ApproachHandleControl.h"


void approach_status_switch(int sta){
    uint32_t data = 0;
    data = (sta << 4) + 0;
    xQueueSend(approach_handle_queue, &data, (TickType_t)0);
}