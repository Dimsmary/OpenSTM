#include "ScanHandle.h"

QueueHandle_t scan_handle_queue;
TaskHandle_t scan_handle;
int scan_last_approach_status;

// Buffer for UART commucation
char scan_output[50] = "";

// Runtime
int last_runtime;

// parameters for line test
int line_test_target;
int line_current_pos;
int line_test_origin_x = 32768;
int line_test_origin_y = 32768;
int line_inc;
char scan_ccch_mode = 0;
bool line_direction_xy;
bool line_direction_fb;
bool line_first_test = true;

// parameters for scan
int scan_x;
int scan_y;
int scan_x_begin;
int scan_x_end;
int scan_y_begin;
int scan_y_end;
int scan_increment;
int scan_cc_increment = 1;
bool scan_forward;
char scan_mode = 0;
int scan_retract;
int scan_final_err = 0;
char scan_ez_switch = 0;

// parameters of delay and status
uint16_t scan_delay = 100;
uint8_t scan_status = 0;

// parameters from approachHandle

extern int current_z_position;
extern int status;
extern int crash;
extern int target;

void scanH_init(){
    xTaskCreatePinnedToCore(scanH_task, "scan_handle_task", 
    1024*3, NULL, configMAX_PRIORITIES - PRIORITY_SCAN, 
    &scan_handle, CORE_SCAN);
}

void scan_exit(char *prefix){
    // Switch back for approach
    scan_status = 0;
    scan_delay = 100;
    approach_status_switch(scan_last_approach_status);
    // Return OK to computer
    cformat_return_value(prefix, 0, scan_output, sizeof(scan_output));
    UARTS_write(scan_output);
    // Return runtime to computer
    int runtime = esp_timer_get_time()/1000 - last_runtime;
    cformat_return_value(RUN_TIME, runtime, scan_output, sizeof(scan_output));
    UARTS_write(scan_output);
}

void line_reverse(){
    // reverse scan direction
    if (line_first_test)
    {
        line_direction_fb = !line_direction_fb;
        line_first_test = false;
        if(line_direction_xy){
            line_test_target = line_test_origin_x;
        }
        else{
            line_test_target = line_test_origin_y;
        }
    }
    else{
        scan_exit(SCAN_LINE_OK);
    }
}

int scan_cc_extend(){
    int read = 0;
    // Read adc
    read = adda_ad_write(ADS8689_NOP, 0, 0);
    read = adda_ad_write(ADS8689_NOP, 0, 0);

    // remapping the read value
    read = read - 32768;
    if(read < 0){
        read = -read;
    }

    while (read < target)
    {
        current_z_position = current_z_position + scan_cc_increment;
        // Return maximum number of read, make program into re-approach mode
        if(current_z_position > 65535){
            return 0;
        }
        ad5761_write(CMD_WR_UPDATE_DAC_REG, current_z_position, DA_Z);

        // Read adc
        read = adda_ad_write(ADS8689_NOP, 0, 0);
        read = adda_ad_write(ADS8689_NOP, 0, 0);

        // remapping the read value
        read = read - 32768;
        if(read < 0){
            read = -read;
        }
    }
    // Retract the tip
    current_z_position = current_z_position - scan_retract;
    if(current_z_position < 0){
        return 0;
    }
    ad5761_write(CMD_WR_UPDATE_DAC_REG, current_z_position, DA_Z);
    
    //Record final errors
    scan_final_err = target - read;
    // return final error
    return read;
}

void scanH_task(void *arg){
    scan_handle_queue = xQueueCreate(SCAN_QUEUE_LENGTH, SCAN_QUEUE_SIZE);
    while (1)
    {   
        // --              --  //
        // --> Line Test（CH） //
        // --              -- //
        if(scan_status == 1){
            // -- X/Y position update -- //
            // true: X, false: Y
            if(line_direction_xy){
                ad5761_write(CMD_WR_UPDATE_DAC_REG, line_current_pos, DA_X);
            }
            else{
                ad5761_write(CMD_WR_UPDATE_DAC_REG, line_current_pos, DA_Y);
            }

            int read;
            // -- Const Current Mode -- //
            if(scan_ccch_mode == 1){
                // get Z position and current
                read = scan_cc_extend();
                if(line_first_test){
                    // Forward direction line data upload
                    cformat_return_value(SCAN_LINE_POSITION, line_current_pos, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    if(scan_ez_switch == 1){
                        cformat_return_value(SCAN_LINE_CURRENT, current_z_position, scan_output, sizeof(scan_output));
                    }
                    else{
                        cformat_return_value(SCAN_LINE_CURRENT, scan_final_err, scan_output, sizeof(scan_output));
                    }
                    
                    UARTS_write(scan_output);
                }else{
                    // Backward direction line data upload
                    cformat_return_value(SCAN_LINE_POSITION_1, line_current_pos, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    if(scan_ez_switch == 1){
                        cformat_return_value(SCAN_LINE_CURRENT_1, current_z_position, scan_output, sizeof(scan_output));
                    }
                    else{
                        cformat_return_value(SCAN_LINE_CURRENT_1, scan_final_err, scan_output, sizeof(scan_output));
                    }
                    UARTS_write(scan_output);
                }
            }
            // -- Const Height Mode -- //
            else{
                // Read Current
                read = adda_ad_write(ADS8689_NOP, 0, 0);
                read = adda_ad_write(ADS8689_NOP, 0, 0);
                // Print position and current
                if(line_first_test){
                    // Forward direction line data upload
                    cformat_return_value(SCAN_LINE_POSITION, line_current_pos, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    cformat_return_value(SCAN_LINE_CURRENT, read, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                }else{
                    // Backward direction line data upload
                    cformat_return_value(SCAN_LINE_POSITION_1, line_current_pos, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    cformat_return_value(SCAN_LINE_CURRENT_1, read, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                }
                // turn the 16bit data into binary
                read = read - 32768;

                // get absolute number of read
                if (read < 0)
                {
                    read = -read;
                }

            }

            // -- Update the postion or exit -- //
            // Crash Limit EXIT
            if(read > crash){
                scan_exit(SCAN_LINE_OK);
            }
            else{
                // forward
                if(line_direction_fb){
                    if (line_current_pos < line_test_target)
                    {
                        line_current_pos += line_inc;
                    }
                    else{
                        // reverse scan direction
                        if (line_first_test)
                        {
                            line_direction_fb = !line_direction_fb;
                            line_first_test = false;
                            if(line_direction_xy){
                                line_test_target = line_test_origin_x;
                            }
                            else{
                                line_test_target = line_test_origin_y;
                            }
                        }
                        else{
                            line_reverse();
                        }
                    }
                }
                // backward
                else{
                    if (line_current_pos > line_test_target)
                    {
                        line_current_pos -= line_inc;
                    }
                    else{
                        line_reverse();
                    }
                }
            }
        }


        // --              --  //
        // --> Image Scan     //
        // --              -- //
        else if(scan_status == 2){
            // update the position
            ad5761_write(CMD_WR_UPDATE_DAC_REG, scan_x, DA_X);
            ad5761_write(CMD_WR_UPDATE_DAC_REG, scan_y, DA_Y);


            int read = 0;
            // Print position and current
            if(scan_forward){
                if(scan_ccch_mode == 1){
                    read = scan_cc_extend();
                    cformat_return_value(SCAN_POS_X, scan_x, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    cformat_return_value(SCAN_POS_Y, scan_y, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    if(scan_ez_switch == 1){
                        cformat_return_value(SCAN_CURRENT, current_z_position, scan_output, sizeof(scan_output));
                    }
                    else{
                        cformat_return_value(SCAN_CURRENT, scan_final_err, scan_output, sizeof(scan_output));
                    }
                    cformat_return_value(SCAN_CURRENT, read, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                }
                else{
                    // Read Tunneling Current
                    // Read twice to achieve latest value
                    read = adda_ad_write(ADS8689_NOP, 0, 0);
                    read = adda_ad_write(ADS8689_NOP, 0, 0);
                    cformat_return_value(SCAN_POS_X, scan_x, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    cformat_return_value(SCAN_POS_Y, scan_y, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    cformat_return_value(SCAN_CURRENT, read, scan_output, sizeof(scan_output));
                    UARTS_write(scan_output);
                    // turn the 16bit data into binary
                    read = read - 32768;

                    // get absolute number of read
                    if (read < 0)
                    {
                        read = -read;
                    }
                }
            }
            

            // Crash exit 
            if(read > crash){
                // scan_exit(SCAN_OK);
                ad5761_write(CMD_WR_UPDATE_DAC_REG, current_z_position - 1000, DA_Z);
            }
            // update the position
            {
                // if direction is forward
                if(scan_forward){
                    // increase the x position
                    scan_x += scan_increment;
                    // if x is overrange
                    if(scan_x > scan_x_end){
                        scan_x -= scan_increment;
                        scan_forward = false;
                        // TEST----------!!!
                        // scan_y += scan_increment;
                        // if (scan_y > scan_y_end){
                        //     scan_exit(SCAN_OK);
                        // }
                        // TEST----------!!!
                    }
                }
                // if direction is backward
                else{
                    // decrease the x position
                    scan_x -= scan_increment;
                    // if x is overrange
                    if(scan_x < scan_x_begin){
                        scan_x += scan_increment;
                        scan_forward = true;
                        scan_y += scan_increment;
                        if(scan_y > scan_y_end){
                            scan_exit(SCAN_OK);
                        }
                    }
                }
            }
        }

        // --                     -- //
        // --> Command handle logic  //
        // --                     -- //
        // queue receive
        uint32_t rcvBuffer = 0xFF;
        xQueueReceive(scan_handle_queue, &(rcvBuffer), 0);

        u_int8_t command = rcvBuffer & 0xFF;
        u_int16_t data = (rcvBuffer >> 8) & 0xFFFF;

        // Command process
        if(command == 0){
            scan_status = data;
            // Line Scan
            if(data == 1){
                // init the position
                ad5761_write(CMD_WR_UPDATE_DAC_REG, line_test_origin_x, DA_X);
                ad5761_write(CMD_WR_UPDATE_DAC_REG, line_test_origin_y, DA_Y);
                // terminate approach procedure
                scan_last_approach_status = status;
                approach_status_switch(0);
                line_first_test = true;

                // Const Current Mode
                if(scan_ccch_mode == 1){
                    current_z_position = current_z_position - 2000;
                    ad5761_write(CMD_WR_UPDATE_DAC_REG, current_z_position, DA_Z);
                }

                // Record Current Time
                last_runtime = esp_timer_get_time() / 1000;
            }
            else if(data == 2){
                // init the position
                scan_x = scan_x_begin;
                scan_y = scan_y_begin;
                // terminate approach procedure
                scan_last_approach_status = status;
                if(scan_ccch_mode == 1){
                    current_z_position = current_z_position - 1000;
                    ad5761_write(CMD_WR_UPDATE_DAC_REG, current_z_position, DA_Z);
                }

                approach_status_switch(0);
                scan_forward = true;
                last_runtime = esp_timer_get_time() / 1000;
            }
            cformat_return_value(SCAN_REG, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 1){
            scan_delay = data;
            cformat_return_value(SCAN_DELAY, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        // Line test command
        else if(command == 2){
            line_test_target = data;
            cformat_return_value(SCAN_LINE_TARGET, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 3){
            line_test_origin_x = data;
            cformat_return_value(SCAN_LINE_ORIGIN_X, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 4){
            line_test_origin_y = data;
            // update original position
            if (line_direction_xy)
            {
                line_current_pos = line_test_origin_x;
            }else{
                line_current_pos = line_test_origin_y;
            }
            // return uart message
            cformat_return_value(SCAN_LINE_ORIGIN_Y, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }
        else if(command == 5){
            line_inc = data;
            cformat_return_value(SCAN_LINE_INC, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 6){
            // Direction:   1: x, forward
            //              2: x, backward
            //              3: y, forward
            //              4: y, backward
            // True/False:  True: x, forward
            //              False: y, backward
            if(data == 1){
                line_direction_xy = true;
                line_direction_fb = true;
            }
            else if(data == 2){
                line_direction_xy = true;
                line_direction_fb = false;
            }
            else if(data == 3){
                line_direction_xy = false;
                line_direction_fb = true;
            }
            else if(data == 4){
                line_direction_xy = false;
                line_direction_fb = false;
            }
            cformat_return_value(SCAN_LINE_DIRECTION, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }
        else if(command == 7){
            scan_retract = data;
            cformat_return_value(SCAN_RETRACT, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 8){
            scan_ccch_mode = data;
            cformat_return_value(SCAN_CCCH_MODE, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 9){
            scan_x_begin = data;
            cformat_return_value(SCAN_X_BEGIN, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 10){
            scan_x_end = data;
            cformat_return_value(SCAN_X_END, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 11){
            scan_y_begin = data;
            cformat_return_value(SCAN_Y_BEGIN, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 12){
            scan_y_end = data;
            cformat_return_value(SCAN_Y_END, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 13){
            scan_increment = data;
            cformat_return_value(SCAN_INC, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 14){
            scan_cc_increment = data;
            cformat_return_value(SCAN_CC_INC, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 15){
            scan_mode = data;
            cformat_return_value(SCAN_MODE, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        else if(command == 16){
            scan_ez_switch = data;
            cformat_return_value(SCAN_EZ, data, scan_output, sizeof(scan_output));
            UARTS_write(scan_output);
        }

        // Global delay
        if(scan_delay != 0){
            vTaskDelay(scan_delay / portTICK_PERIOD_MS);
        }
        // if scan_delay == 0, then full speed running
        
    }
    
}
