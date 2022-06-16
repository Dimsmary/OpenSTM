#include <Arduino.h>
#include "ad5761.hpp"
#include "ads868x.hpp"
#include "uartcommand.hpp"
#include "steppermotor.hpp"
#include "control.hpp"


// Multi-Thread handle
TaskHandle_t core0_loop_handle;
void core0_loop(void * pvParameters);

// init command receiver, 2 alphabet for command
uartcommand UartCommand(500000, 2);
ADC_ads868x ads868x(1);
controlflow ControlFlow;

void init_adda(){
  // RESET THE ADC AND DAC
  ad5761_reset();
  ads868x.reset();
}


void setup() {
  ad5761_SPI_init();
  stepper_init(9600);

  xTaskCreatePinnedToCore(
                    core0_loop,               /* Task function. */
                    "core0_loop",             /* name of task. */
                    10000,                    /* Stack size of task */
                    NULL,                     /* parameter of the task */
                    1,                        /* priority of the task */
                    &core0_loop_handle,       /* Task handle to keep track of created task */
                    0);                       /* pin task to core 0 */
    delay(500); 
}


// *** Main Loop *** //
void loop() {
  // Read uart command
  UartCommand.read_uart();

  // If a command end with '\n' is received
  if(UartCommand.is_command_finished()){
    String header = UartCommand.get_header();
    int param =UartCommand.get_param();

    // *** COARSE APROACH *** //
    // set motor speed
    if(header == "MS"){
      stepper_set_delay(param);
    }

    // rotate all the motor FORWARD
    else if(header  == "MF"){
      stepper_coarse_approach(true, true);
    }

    // rotate all the motor BACKWARD
    else if(header  == "MB"){
      stepper_coarse_approach(true, false);
    }
    // stop all the motor
    else if(header == "MH"){
      stepper_coarse_approach(false, false);
    }
    // Rotate Single Stepper Motor
    // MOTORA
    else if(header == "M1"){
      if(param == 1){
        stepper_coarse_single(1, false);
      }else{
        stepper_coarse_single(1, true);
      }
    }
    // MOTORB
    else if(header == "M2"){
      if(param == 1){
        stepper_coarse_single(2, false);
      }else{
        stepper_coarse_single(2, true);
      }
    }
    // MOTORB
    else if(header == "M3"){
      if(param == 1){
        stepper_coarse_single(3, false);
      }else{
        stepper_coarse_single(3, true);
      }
    }

    // Fine step forward test
    else if(header == "MQ"){
      stepper_fine_forward(param);
    }

    else if(header == "MW"){
      stepper_fine_backward(param);
    }

    // step forward/backward for a period
    else if(header == "ME"){
      stepper_coarse_single(1, true);
      delay(param);
      stepper_coarse_approach(false, false);
    }

    else if(header == "MR"){
      stepper_coarse_single(1, false);
      delay(param);
      stepper_coarse_approach(false, false);
    }

    else if(header == "MP"){
      stepper_release(param);
    }

    // *** Fine Approach *** //
    // set tunneling limit voltage
    else if(header == "TU"){
      ControlFlow.tunneling_voltage_limit = param;
      UartCommand.return_ok();
    }

    // set tunneling crash limit voltage
    else if(header == "TC"){
      ControlFlow.drawback_voltage_limit = param;
      UartCommand.return_ok();
    }

    // stepper motor forward step
    else if(header == "TF"){
      ControlFlow.forward_step = param;
      UartCommand.return_ok();
    }

    // set piezo forwarad step
    else if(header == "TS"){
      ControlFlow.z_step = param;
      UartCommand.return_ok();
    }

    // set piezo delay
    else if(header == "TD"){
      ControlFlow.z_delay_time = param;
      UartCommand.return_ok();
    }

    // set piezo drawback value
    else if(header == "TP"){
      ControlFlow.piezo_drwaback = param;
      UartCommand.return_ok();
    }

    // set tunneling curve test value
    else if(header == "T1"){
      ControlFlow.z_test_delay_time = param;
      UartCommand.return_ok();
    }

    else if(header == "T2"){
      ControlFlow.z_test_step = param;
      UartCommand.return_ok();
    }

    // approach begin
    else if(header == "TG"){
      ControlFlow.scan_mode = 1;
      ControlFlow.dac_register_z = 0;
      stepper_release(1);
      stepper_release(2);
      UartCommand.return_ok();
    }

    // approach halt
    else if(header == "TH"){
      ControlFlow.scan_mode = 0;
      UartCommand.return_ok();
    }

    else if(header == "TT"){
      ControlFlow.z_scan = true;
    }

    else if(header == "TN"){
      ControlFlow.z_scan = false;
    }

    // *** SCAN!!! *** //
    // set bias end
    else if(header == "IE"){
      ControlFlow.bias_end = param;
    }
    // set bias step
    else if(header == "IS"){
      ControlFlow.bias_step = param;
    }
    else if(header == "IG"){
      ControlFlow.is_bias_test = true;
    }
    else if(header == "IH"){
      ControlFlow.is_bias_test = false;
    }

    // *** SCAN!!! *** //
    
    // set begin range
    else if(header == "SB"){
      ControlFlow.x_min_range = param;
      ControlFlow.y_min_range = param;
      UartCommand.return_ok();
    }

    else if(header == "SE"){
      ControlFlow.x_max_range = param;
      ControlFlow.y_max_range = param;
      UartCommand.return_ok();
    }

    else if(header == "SS"){
      ControlFlow.xy_step = param;
      UartCommand.return_ok();
    }

    else if(header == "SD"){
      ControlFlow.xy_delay_time = param;
      UartCommand.return_ok();
    }

    // begin the scan
    else if(header == "SG"){
      ControlFlow.x_forward = true;
      ControlFlow.y_forward = false;
      ControlFlow.scan_finished = false;
      ControlFlow.dac_register_x = ControlFlow.x_min_range;
      ControlFlow.dac_register_y = ControlFlow.y_min_range;
      ad5761_write(CMD_WR_UPDATE_DAC_REG, ControlFlow.dac_register_x, X_DAC);
      ad5761_write(CMD_WR_UPDATE_DAC_REG, ControlFlow.dac_register_y, Y_DAC);

      if(param == 0){
        ControlFlow.scan_mode = 2;
        ControlFlow.xy_reverse = false;
      }
      else if(param == 1){
        ControlFlow.scan_mode = 2;
        ControlFlow.xy_reverse = true;
      }
      else if(param == 2){
        ControlFlow.scan_mode = 3;
        ControlFlow.xy_reverse = false;
      }
      else if(param == 3){
        ControlFlow.scan_mode = 3;
        ControlFlow.xy_reverse = true;
      }

      
    }

    // terminate the scan
    else if(header == "ST"){
      ControlFlow.scan_mode = 1;
      
    }
  

    // *** DEBUG *** //
    // SET DAC

    // reset command
    else if(header == "RE"){
      init_adda();
    }

    else if(header == "DA"){
      int register_val = param % 100000;
      int cs = (param - register_val) / 100000;
      // update register value for DACs
      if(cs == 2){
        ControlFlow.dac_register_z = register_val;
      }
      else if(cs == 1){
        ControlFlow.dac_register_sample = register_val;
      }
      ad5761_write(CMD_WR_UPDATE_DAC_REG, register_val, cs - 1);
      UartCommand.return_ok();
    }

    // GET ADC
    else if(header == "AD"){
      UartCommand.upload_adc(ads868x.readADC());
    }

  }
}


// *** loop for DAC Scan *** //
void core0_loop(void * pvParameters){
  for(;;){
    ControlFlow.update();
  }
}