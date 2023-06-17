#include "SystemHandle.h"

QueueHandle_t system_handle_quene;
TaskHandle_t system_handle;

void systemH_init(){
    // create Task to handle system command
    xTaskCreatePinnedToCore(systemH_task, "system_handle_task", 
    1024*2, NULL, configMAX_PRIORITIES - PRIORITY_SYSTEM_HANDLE, &system_handle, CORE_SYSTEM_H);
}

void systemH_return_value(char *prefix, int value){
    char output[50] = "";
    strncpy(output, prefix, sizeof(output));
    strcat(output, "-");

    char buff[50];
    sprintf(buff, "%d", value);
    strcat(output, buff);
    UARTS_write(output);
}

void systemH_task(void *arg){
    uint32_t rcvBuffer;
    system_handle_quene = xQueueCreate(SYSTEMH_QUENE_LENGTH, SYSTEMH_QUENE_SIZE);
    while (1){
        if(xQueueReceive(system_handle_quene, &(rcvBuffer), portMAX_DELAY)){
            
            // Split the quene data into command and data
            uint8_t command;
            uint16_t data;
            command = rcvBuffer >> 16;
            data = rcvBuffer & 0xFFFF;
            
            
            switch (command)
            {
            // -> Return system version
            case 0:
                UARTS_write(SYSTEM_VERSION_NOW);
                break;
            // -> Set BIAS(16bit) Voltage
            case 1:
                ad5761_write(CMD_WR_UPDATE_DAC_REG, data, 0);
                systemH_return_value(SYSTEM_COMMAND_SET_16b, data);
                break;

            // -> Set Z Voltage
            case 2:
                ad5761_write(CMD_WR_UPDATE_DAC_REG, data, 1);
                systemH_return_value(SYSTEM_COMMAND_SET_DZ, data);
                break;

            // -> Set Y Voltage
            case 3:
                ad5761_write(CMD_WR_UPDATE_DAC_REG, data, 2);
                systemH_return_value(SYSTEM_COMMAND_SET_DX, data);
                break;

            // -> Set X Voltage
            case 4:
                ad5761_write(CMD_WR_UPDATE_DAC_REG, data, 3);
                systemH_return_value(SYSTEM_COMMAND_SET_DY, data);
                break;

            // -> Set Slider(12bit) Voltage
            case 5:
                adda_12bitda_write(CMD_WR_UPDATE_DAC_REG, data);
                systemH_return_value(SYSTEM_COMMAND_SET_12b, data);
                break;

            // -> Read ADC
            case 6:
                int read = adda_ad_write(ADS8689_NOP, 0, 0);
                systemH_return_value(SYSTEM_GET_ADC, read);
                break;

            default:
                break;
            }
        }
    
    }
}

