#include "control.hpp"

void controlflow::all_status_reset(){
    scan_mode = 0;
    tunneling_established = false;
    command_est_send = false;
    command_crash_send = false;
    z_scan = false;
    is_bias_test = false;
    x_forward = true;
    y_forward = false;
    scan_finished = false;
    xy_reverse = false;
}

controlflow::controlflow(){
    all_status_reset();
}


void controlflow::update(){
    // Check the work condiction
    // ** IDLE ** //
    if(scan_mode == 0){
      delay(1);
    }

    // ** Fine Approach ** //
    else if(scan_mode == 1){
      // Read ADC --> Crash DrackBack     --> TunnelingEstablish = F, drawbackFlag = T
      //          --> Current Established --> TunnelingEstablish = T --> SCAN
      //          --> Approaching         --> Delay --> StepDown
      // read ADC
      uint16_t adc_value = ads868x.readADC();
      UartCommand.upload_dac_z(dac_register_z);
      if(is_bias_test){
        UartCommand.upload_dac_sample(dac_register_sample);
      }
      UartCommand.upload_adc(adc_value);

      // *** CRASH THRESHOLD *** //
      if(adc_value > drawback_voltage_limit){
        // piezo drawback
        dac_register_z = dac_register_z - piezo_drwaback;

        // if piezo drawback is out of range
        if(dac_register_z < 0){
          // stepper quick drawback
          stepper_set_delay(2);
          stepper_coarse_single(1, false);
          delay(200);
          stepper_coarse_approach(false, false);
          
          //reset dac-z
          dac_register_z = 0;
        }

        ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_z, Z_DAC);
        
        // set flag
        tunneling_established = false;
        z_scan = false;
        is_bias_test = false;

        // send status to computer
        if(!command_crash_send){
          Serial.println("CR0");
          command_crash_send = true;
        }
        delay(z_delay_time);
      }

      // *** TUNNELING ESTABLISHED THRESHOLD *** //
      else if(adc_value > tunneling_voltage_limit){
        // set the flag
        tunneling_established = true;

        // send command to computer
        if(!command_est_send){
          Serial.println("DO0");
          command_est_send = true;
        }
        
        // test tunneling current curve
        if(z_scan){
          dac_register_z = dac_register_z + z_test_step;
          ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_z, Z_DAC);
          delay(z_test_delay_time);
        }
        else if(is_bias_test){
          if(dac_register_sample > bias_end){
            dac_register_sample = dac_register_sample - bias_step;
          }
          else{
            dac_register_sample = dac_register_sample + bias_step;
          }
          ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_sample, SAM_DAC);
          delay(1);
        }
        else{
          delay(z_delay_time);
        }
      }

      // *** Z APPRAOCING *** //
      else{
        // reset send commend flag
        command_est_send = false;
        command_crash_send = false;
        delay(z_delay_time);
        // step down the piezo buzzer
        dac_register_z = dac_register_z + z_step;

        // if piezo buzzer position is maximum
        if(dac_register_z > 65535){
          dac_register_z = 0;
          stepper_fine_forward(forward_step);
        }
        // upadte the DAC
        ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_z, Z_DAC);
      }
    }

    else if(scan_mode == 2){
        //**************** SCAN CODE HERE *********************//
        UartCommand.upload_dac_x(dac_register_x);
        UartCommand.upload_dac_y(dac_register_y);
        UartCommand.upload_adc(ads868x.readADC()); 

        if(x_forward){
          dac_register_x = dac_register_x + xy_step;
          if(dac_register_x > x_max_range){
            dac_register_x = dac_register_x - 2 * xy_step;
            x_forward = false;
            y_forward = true;
          }
        }
        else{
          dac_register_x = dac_register_x - xy_step;
          if(dac_register_x < x_min_range){
            dac_register_x = dac_register_x + 2 * xy_step;
            x_forward = true;
            y_forward = true;
          }
        }

        if(y_forward){
          dac_register_y = dac_register_y + xy_step;
          if(dac_register_y > y_max_range){
            dac_register_y = dac_register_y - xy_step;
            scan_mode = 1;
          }
          y_forward = false;
        }


        if(xy_reverse){
          ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_x, Y_DAC);
          ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_y, X_DAC);
        }
        else{
          // update DAC value
          ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_x, X_DAC);
          ad5761_write(CMD_WR_UPDATE_DAC_REG, dac_register_y, Y_DAC);
          
        }
        delayMicroseconds(xy_delay_time);
    }
}

