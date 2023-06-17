#include "CommandDistribute.h"

QueueHandle_t command_distribute_quene;

void commandD_to_systemH(uint8_t command, char *data){
    uint32_t sendbuff;

    // send command and data to system Handle
    sendbuff = (command << 16) | atoi(data);
    xQueueSend(system_handle_quene, &sendbuff, (TickType_t)0);
}

void commandD_task(void *arg){
    // Create a buffer to receive queue data
    char rcvBuffer[COMMAND_QUENE_SIZE];
    char commandBuffer[COMMAND_LENGTH + 1];
    char dataBuffer[DATA_LENGTH + 1];

    // init the quene
    command_distribute_quene = xQueueCreate(COMMAND_QUENE_LENGTH, COMMAND_QUENE_SIZE);
    while (1){
        if(xQueueReceive(command_distribute_quene, &(rcvBuffer), portMAX_DELAY)){
            // split the command
            memcpy(commandBuffer, rcvBuffer, 5);
            commandBuffer[COMMAND_LENGTH + 1] = '\0';
            memcpy(dataBuffer, &rcvBuffer[5], 5);
            dataBuffer[DATA_LENGTH + 1] = '\0';
            
            // distribute the command and data
            // -> System Handle
            if(strcmp(commandBuffer, SYSTEM_VERSION) == 0){
                commandD_to_systemH(0, dataBuffer);
            }
            else if(strcmp(commandBuffer, SYSTEM_COMMAND_SET_16b) == 0){
                commandD_to_systemH(1, dataBuffer);
            }
            else if(strcmp(commandBuffer, SYSTEM_COMMAND_SET_DZ) == 0){
                commandD_to_systemH(2, dataBuffer);
            }
            else if(strcmp(commandBuffer, SYSTEM_COMMAND_SET_DX) == 0){
                commandD_to_systemH(3, dataBuffer);
            }
            else if(strcmp(commandBuffer, SYSTEM_COMMAND_SET_DY) == 0){
                commandD_to_systemH(4, dataBuffer);
            }
            else if(strcmp(commandBuffer, SYSTEM_COMMAND_SET_12b) == 0){
                commandD_to_systemH(5, dataBuffer);
            }
            else if(strcmp(commandBuffer, SYSTEM_GET_ADC) == 0){
                commandD_to_systemH(6, dataBuffer);
            }
            // -> Curve Handle
            else if(strcmp(commandBuffer, CURVE_STATUS) == 0){
                int data = atoi(dataBuffer);
                xQueueSend(curve_handle_queue, &data, (TickType_t)0);
            }

            // -> Approach Handle
            else if(strcmp(commandBuffer, APPROACH_REGISTER) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 0;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }

            else if(strcmp(commandBuffer, APPROACH_SLIDER_STEP) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 1;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }

            else if(strcmp(commandBuffer, APPROACH_SET_KP) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 2;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }

            else if(strcmp(commandBuffer, APPROACH_SET_KI) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 3;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_SET_KD) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 4;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_TARGET) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 5;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_CRASH) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 6;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_S_AMPLITUDE) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 7;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_S_SLOPE) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 8;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_S_FAST) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 9;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_S_SLOW) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 10;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, APPROACH_BIAS) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 11;
                xQueueSend(approach_handle_queue, &data, (TickType_t)0);
            }

            // -> Curve Test Handle
            else if(strcmp(commandBuffer, CURVE_TEST_REG) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 0;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, CURVE_TEST_DI_STOP) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 1;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, CURVE_TEST_DI_INCREMENT) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 2;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, CURVE_TEST_BI_STOP) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 3;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, CURVE_TEST_BI_INCREMENT) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 4;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, CURVE_TEST_RESET) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 5;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, CURVE_TEST_DELAY) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 6;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, CURVE_TEST_BI_START) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 4) & 0xFFFF0) + 7;
                xQueueSend(curve_test_handle_queue, &data, (TickType_t)0);
            }

            // -> Scan Image handle
            else if(strcmp(commandBuffer, SCAN_REG) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 0;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_DELAY) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 1;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_LINE_TARGET) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 2;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_LINE_ORIGIN_X) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 3;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_LINE_ORIGIN_Y) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 4;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_LINE_INC) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 5;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }

            else if(strcmp(commandBuffer, SCAN_LINE_DIRECTION) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 6;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }

            else if(strcmp(commandBuffer, SCAN_RETRACT) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 7;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_CCCH_MODE) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 8;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            // Scan
            else if(strcmp(commandBuffer, SCAN_X_BEGIN) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 9;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_X_END) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 10;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_Y_BEGIN) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 11;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_Y_END) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 12;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_INC) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 13;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_CC_INC) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 14;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_MODE) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 15;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }
            else if(strcmp(commandBuffer, SCAN_EZ) == 0){
                uint32_t data = atoi(dataBuffer);
                data = ((data << 8) & 0xFFFF00) + 16;
                xQueueSend(scan_handle_queue, &data, (TickType_t)0);
            }

        }
    }
}

void commandD_init(){
    // create Task to distribute
    xTaskCreatePinnedToCore(commandD_task, "command_distribute_task", 
    1024*2, NULL, configMAX_PRIORITIES - PRIORITY_COMMAND_DISTRIBUTE, NULL, CORE_COMMAND);

    // init system handle
    systemH_init();

    // init curve handle
    curveH_init();

    // init approach handle
    approachH_init();

    // init curve test handle
    curve_test_init();

    // init scan handle
    scanH_init();
}
