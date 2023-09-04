#include "ApproachHandle.h"

QueueHandle_t approach_handle_queue;
TaskHandle_t approach_handle;
int current_z_position = 0;
int target = 0;
float kp = 0.005;
float ki = 0;
float kd = 0;
int status = 0;
char output[50] = "";
int step = 10;
int crash = 0;
int err_acc = 0;
int err_last = 0;
int triangle_amplitude = 4095;
int triangle_slope = 16;
int cap_fast_limit = 0;
int cap_slow_limit = 0;
int bias_voltage = 0;

void approachH_init(){
    xTaskCreatePinnedToCore(approacH_task, "approach_handle_task", 
    1024*3, NULL, configMAX_PRIORITIES - PRIORITY_APPROACH_HANDLE, 
    &approach_handle, CORE_APPROACH);
}

int triangle_Wave_forward(int step, int amp, int inc){
    uint16_t data = 0;
    int read;
    // Generate Triangle Wave
    while(step > 0){
        data = 4095 - amp;
        while (data < 4095)
        {
            adda_12bitda_write(CMD_WR_UPDATE_DAC_REG, ~data << 4);
            data += inc;
        }
        
        data = 4095 - amp;
        adda_12bitda_write(CMD_WR_UPDATE_DAC_REG, ~data << 4);
        step --;
    }

    // measure voltage output
    read = adda_ad_write(ADS8689_NOP, 0, 0);
    read = adda_ad_write(ADS8689_NOP, 0, 0);

    // turn the 16bit data into binary
    read = read - 32768;

    // get absolute number of read
    if (read < 0)
    {
        read = -read;
    }
    return read;
}

void triangle_Wave_backward(int step, int amp, int inc){
    uint16_t data;
    // Generate Triangle Wave
    while(step > 0){
        data = 4095 - amp;
        while (data < 4095)
        {
            adda_12bitda_write(CMD_WR_UPDATE_DAC_REG, data << 4);
            data += inc;
        }
        
        data = 4095 - amp;
        adda_12bitda_write(CMD_WR_UPDATE_DAC_REG, data << 4);
        step --;
    }
        
}

bool z_scan(int target){
    // init z position is 0, tip retract
    int z_position = 0;
    ad5761_write(CMD_WR_UPDATE_DAC_REG, z_position, DA_Z);
    while (1)
    {   
        // Read adc
        int read = adda_ad_write(ADS8689_NOP, 0, 0);
        read = adda_ad_write(ADS8689_NOP, 0, 0);

        // remapping the read value
        read = read - 32768;
        if(read < 0){
            read = -read;
        }

        if(read < target){
            z_position = z_position + 50;
            if(z_position > 65535){
                return false;
            }
            ad5761_write(CMD_WR_UPDATE_DAC_REG, z_position, DA_Z);
            vTaskDelay(1);
        }
        else{
            //recored current Z position
            current_z_position = z_position;
            return true;
        }
        
    }
}

void approacH_task(void *arg){
    approach_handle_queue = xQueueCreate(APPROACH_QUEUE_LENGTH, APPROACH_QUEUE_SIZE);
    ad5761_write(CMD_WR_UPDATE_DAC_REG, current_z_position, DA_Z);
    while (1)
    {   
        // --> 1: Get into FAST mode
        if(status == 1){
            // Slider Begin, Fast Mode
            // forward 1 step, and read punch
            int punch = triangle_Wave_forward(1, 4095, 64);
            cformat_return_value(APPROACH_RETURN_PUNCH, punch, output, sizeof(output));
            UARTS_write(output);
            if(punch > cap_slow_limit){
                status = 5;
                ad5761_write(CMD_WR_UPDATE_DAC_REG, bias_voltage, DA_BIAS);
                // turn to Z scan mode
                cformat_return_value(APPROACH_RETURN_STATUS, status, output, sizeof(output));
                UARTS_write(output);
            }
            else if(punch > cap_fast_limit){
                status = 4;
                // turn to slow mode
                cformat_return_value(APPROACH_RETURN_STATUS, status, output, sizeof(output));
                UARTS_write(output);
            }
        }
        // --> 2: Get into Continous FORWARD mode
        else if(status == 2){
            int punch = triangle_Wave_forward(step, triangle_amplitude, triangle_slope);
            cformat_return_value(APPROACH_RETURN_PUNCH, punch, output, sizeof(output));
            UARTS_write(output);
            status = 0;
        }
        // --> 3: Get into Continous RETRACT mode
        else if(status == 3){
            triangle_Wave_backward(step, triangle_amplitude, triangle_slope);
            status = 0;
        }

        // --> 4: SLOW mode
        else if (status == 4)
        {   
            int punch = triangle_Wave_forward(1, triangle_amplitude, triangle_slope);
            cformat_return_value(APPROACH_RETURN_PUNCH, punch, output, sizeof(output));
            UARTS_write(output);
            if(punch > cap_slow_limit){
                status = 5;
                ad5761_write(CMD_WR_UPDATE_DAC_REG, bias_voltage, DA_BIAS);
                // turn to Z scan mode
                cformat_return_value(APPROACH_RETURN_STATUS, status, output, sizeof(output));
                UARTS_write(output);
            }
        }

        // --> 5: Z scan mode
        else if(status == 5){
            bool is_est = z_scan(target);
            if (!is_est)
            {   
                status = 4;
                // back to slow mode
                cformat_return_value(APPROACH_RETURN_STATUS, status, output, sizeof(output));
                UARTS_write(output);
            }
            else{
                status = 6;
                // turn to PID mode
                cformat_return_value(APPROACH_RETURN_STATUS, status, output, sizeof(output));
                UARTS_write(output);
            }
        }

        // -->: PID Mode
        else if(status == 6){
            // Read adc
            int read = adda_ad_write(ADS8689_NOP, 0, 0);
            read = adda_ad_write(ADS8689_NOP, 0, 0);
            // remapping the read value
            read = read - 32768;
            if(read < 0){
                read = -read;
            }
            // Execute PID
            int err = target - read;
            cformat_return_value(SYSTEM_GET_ADC, read, output, sizeof(output));
            UARTS_write(output);
            if(abs(err) > 400){
                // PID calculate
                int increase_step = (err*kp) + (err_acc * ki) + (err_last * kd);

                current_z_position = current_z_position + increase_step;
                // if scanner is out of range
                if (current_z_position > 65535){   
                    // set back to mode1
                    current_z_position = 0;
                    status = 4;
                    // turn to slow mode
                    cformat_return_value(APPROACH_RETURN_STATUS, status, output, sizeof(output));
                    UARTS_write(output);
                }
                else if(current_z_position < 0){
                    triangle_Wave_backward(10, triangle_amplitude, triangle_slope);
                    current_z_position = 0;
                    status = 4;
                    // turn to slow mode
                    cformat_return_value(APPROACH_RETURN_STATUS, status, output, sizeof(output));
                    UARTS_write(output);
                }
                else{
                    ad5761_write(CMD_WR_UPDATE_DAC_REG, current_z_position, DA_Z);
                }
                cformat_return_value(APPROACH_RETURN_PID, increase_step, output, sizeof(output));
                UARTS_write(output);
                err_acc = err_acc + err;
                err_last = err;
            }else{
                // clear PID parameters
                err_acc = 0;
                err_last = 0;
            }
        }

        vTaskDelay(1); 
        
        // queue receive
        uint32_t rcvBuffer = 0xF;
        xQueueReceive(approach_handle_queue, &(rcvBuffer), 0);

        u_int8_t command = rcvBuffer & 0xF;
        u_int16_t data = (rcvBuffer >> 4) & 0xFFFF;
        if (command == 0)
        {
            status = data;
            cformat_return_value(APPROACH_REGISTER, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 1){
            step = data;
            cformat_return_value(APPROACH_SLIDER_STEP, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 2){
            kp = data;
            kp = kp/10000;
            cformat_return_value(APPROACH_SET_KP, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 3){
            ki = data;
            ki = ki/10000;
            cformat_return_value(APPROACH_SET_KI, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 4){
            kd = data;
            kd = kd/10000;
            cformat_return_value(APPROACH_SET_KD, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 5){
            target = data;
            target = target - 32768;
            if(target < 0){
                target = -target;
            }
            cformat_return_value(APPROACH_TARGET, target, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 6){
            crash = data;
            crash = crash - 32768;
            if(crash < 0){
                crash = -crash;
            }
            cformat_return_value(APPROACH_CRASH, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 7){
            triangle_amplitude = data;
            cformat_return_value(APPROACH_S_AMPLITUDE, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 8){
            triangle_slope = data;
            cformat_return_value(APPROACH_S_SLOPE, data, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 9){
            cap_fast_limit = data;
            cap_fast_limit = cap_fast_limit;
            cformat_return_value(APPROACH_S_FAST, cap_fast_limit, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 10){
            cap_slow_limit = data;
            cap_slow_limit = cap_slow_limit;
            cformat_return_value(APPROACH_S_SLOW, cap_slow_limit, output, sizeof(output));
            UARTS_write(output);
        }
        else if(command == 11){
            // set bias voltage
            bias_voltage = data;
            ad5761_write(CMD_WR_UPDATE_DAC_REG, bias_voltage, DA_BIAS);
            cformat_return_value(APPROACH_BIAS, data, output, sizeof(output));
            UARTS_write(output);
        }
    }
    
}
