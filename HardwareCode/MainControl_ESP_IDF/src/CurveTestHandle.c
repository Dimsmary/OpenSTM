#include "CurveTestHandle.h"

QueueHandle_t curve_test_handle_queue;
TaskHandle_t curve_test_handle;

int curve_status;
char curve_output[50] = "";

// DI test parameters
int curve_z_position;
uint16_t curve_di_value;
int curve_di_stop_point;
uint16_t curve_di_increment;

// Bias test parameters
uint16_t curve_bias_stop_point;
uint16_t curve_bias_increment;
uint16_t curve_bias_start_point;
int curve_bias_voltage;


// delay
int curve_delay = 100;

// Approach handle status
int last_approach_status = 0;
// parameters from approachHandle
extern int current_z_position;
extern int status;
extern int crash;
extern int bias_voltage;

void curve_test_init(){
    xTaskCreatePinnedToCore(curve_test_task, "curve_test_handle_task", 
    1024*3, NULL, configMAX_PRIORITIES - PRIORITY_CURVE_TEST, 
    &curve_test_handle, CORE_CURVE_TEST);
}


void curve_test_task(void *arg){
    curve_test_handle_queue = xQueueCreate(CURVE_TEST_QUEUE_LENGTH, CURVE_TEST_QUEUE_SIZE);
    while (1)
    {   

        // --> Z Scan
        if(curve_status == 1){
            // -- Z position update -- //
            ad5761_write(CMD_WR_UPDATE_DAC_REG, curve_z_position, DA_Z);

            // -- Read Current -- //
            int read;
            read = adda_ad_write(ADS8689_NOP, 0, 0);
            read = adda_ad_write(ADS8689_NOP, 0, 0);

            // Pint z position
            cformat_return_value(CURVE_TEST_DI_ZPOS, curve_z_position, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);

            // Pint current
            cformat_return_value(CURVE_TEST_DI_CURRENT, read, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);

            // turn the 16bit data into binary
            read = read - 32768;

            // get absolute number of read
            if (read < 0)
            {
                read = -read;
            }

            // -- Update the postion of z or Exit -- //
            if(read > curve_di_stop_point){
                curve_status = 0;
                cformat_return_value(CURVE_TEST_DI_OK, 0, curve_output, sizeof(curve_output));
                UARTS_write(curve_output);
                curve_delay = 100;
                approach_status_switch(last_approach_status);
            }
            else{
                curve_z_position += curve_di_increment;
                // if z is overange
                if(curve_z_position > 65535){
                    curve_status = 0;
                    cformat_return_value(CURVE_TEST_DI_OK, 0, curve_output, sizeof(curve_output));
                    UARTS_write(curve_output);
                    curve_delay = 100;
                    approach_status_switch(last_approach_status);
                }
            }

        }
        // --> Bias Test
        else if(curve_status == 2){
            // -- Switch Bias -- //
            ad5761_write(CMD_WR_UPDATE_DAC_REG, curve_bias_voltage, DA_BIAS);

            // -- Read Current -- //
            int read;
            read = adda_ad_write(ADS8689_NOP, 0, 0);
            read = adda_ad_write(ADS8689_NOP, 0, 0);

            // Pint bias voltage
            cformat_return_value(CURVE_TEST_BI_BIAS, curve_bias_voltage, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);

            // Pint current
            cformat_return_value(CURVE_TEST_BI_CURRENT, read, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);


            // turn the 16bit data into binary
            read = read - 32768;

            // get absolute number of read
            if (read < 0)
            {
                read = -read;
            }

            // -- Update the BIAS or Exit -- //
            if(read > crash){
                curve_status = 0;
                cformat_return_value(CURVE_TEST_BI_OK, 0, curve_output, sizeof(curve_output));
                UARTS_write(curve_output);
                curve_delay = 100;
                ad5761_write(CMD_WR_UPDATE_DAC_REG, bias_voltage, DA_BIAS);
                approach_status_switch(last_approach_status);
            }
            else{
                curve_bias_voltage += curve_bias_increment;
                // if z is overange
                if(curve_bias_voltage > curve_bias_stop_point){
                    curve_status = 0;
                    cformat_return_value(CURVE_TEST_BI_OK, 0, curve_output, sizeof(curve_output));
                    UARTS_write(curve_output);
                    curve_delay = 100;
                    ad5761_write(CMD_WR_UPDATE_DAC_REG, bias_voltage, DA_BIAS);
                    approach_status_switch(last_approach_status);
                }
            }
        }


        // --> Command handle logic
        // queue receive
        uint32_t rcvBuffer = 0xF;
        xQueueReceive(curve_test_handle_queue, &(rcvBuffer), 0);

        u_int8_t command = rcvBuffer & 0xF;
        u_int16_t data = (rcvBuffer >> 4) & 0xFFFF;
        

        // Command resolve
        if (command == 0){
            curve_status = data;
            cformat_return_value(CURVE_TEST_REG, data, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }

        // D-I test
        else if (command == 1){
            // update target
            curve_di_stop_point = data;
            curve_di_stop_point = curve_di_stop_point - 32768;
            if(curve_di_stop_point < 0){
                curve_di_stop_point = -curve_di_stop_point;
            }
            cformat_return_value(CURVE_TEST_DI_STOP, curve_di_stop_point, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }

        else if (command == 2){
            curve_di_increment = data;
            cformat_return_value(CURVE_TEST_DI_INCREMENT, data, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }
        
        // Bias Test
        else if (command == 3){
            curve_bias_stop_point = data;
            cformat_return_value(CURVE_TEST_BI_STOP, data, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }

        else if(command == 4){
            curve_bias_increment = data;
            cformat_return_value(CURVE_TEST_BI_INCREMENT, data, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }

        else if(command == 7){
            curve_bias_start_point = data;
            cformat_return_value(CURVE_TEST_BI_START, data, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }

        // Reset
        else if (command == 5){
            
            // If reset for DI test
            if(data == 0){
                // update position
                curve_z_position = current_z_position;
                if (curve_z_position < 0)
                {
                    curve_z_position = 0;
                }
                
                // restore approach mode status
                last_approach_status = status;
                // switch approach mode to IDLE
                approach_status_switch(0);
            }
            //  If reset for BIAS test
            else if(data == 1){
                curve_bias_voltage = curve_bias_start_point;

                // restore approach mode status
                last_approach_status = status;
                // switch approach mode to IDLE
                approach_status_switch(0);
            }
            cformat_return_value(CURVE_TEST_RESET, data, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }

        else if (command == 6){
            curve_delay = data;
            cformat_return_value(CURVE_TEST_DELAY, data, curve_output, sizeof(curve_output));
            UARTS_write(curve_output);
        }
        
        // Global delay
        if(curve_delay != 0){
            vTaskDelay(curve_delay / portTICK_PERIOD_MS);
        }
    }
    
}
