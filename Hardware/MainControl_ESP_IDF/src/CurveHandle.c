#include "CurveHandle.h"

QueueHandle_t curve_handle_queue;
TaskHandle_t curve_handle;

void curveH_init(){
    xTaskCreate(curveH_task, "curve_handle_task", 
    1024*2, NULL, configMAX_PRIORITIES - PRIORITY_CURVE_HANDLE, &curve_handle);
}

void curveH_task(void *arg){
    curve_handle_queue = xQueueCreate(CURVE_QUEUE_LENGTH, CURVE_QUEUE_SIZE);
    uint16_t rcvBuf = 0x3E8;
    char output[50] = "";
    while (1)
    {   
        // update queue data
        xQueueReceive(curve_handle_queue, &rcvBuf, 0);
        
        // if bit16 is 1
        if((rcvBuf >> 15) & 0x1){
            // transmit the adc data
            int read = adda_ad_write(ADS8689_NOP, 0, 0);
            cformat_return_value("GETAD", read, output, sizeof(output));
            UARTS_write(output);
        }
        // delay
        int delaytime = rcvBuf & 0x7fff;
        vTaskDelay(delaytime / portTICK_PERIOD_MS);
    }
    
}

