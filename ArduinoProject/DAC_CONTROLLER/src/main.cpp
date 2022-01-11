#include <Arduino.h>

#include "init.h"
#include "touch_cal.hpp"
#include "lvgl_control.hpp"
#include "ad5761.hpp"


extern byte SPI_Buff[];

// Invoke the TFT library and creat a instant
TFT_eSPI tft = TFT_eSPI();

// multitask: DAC Write
void multitask_dac_update(void * parameters){
    for(;;){
        if(approach_get_z_power()){
        ad5761_write(CMD_WR_UPDATE_DAC_REG, approach_get_z_register(), 0);
    }

    if(approach_get_tip_power()){
        ad5761_write(CMD_WR_UPDATE_DAC_REG, approach_get_tip_register(), 1);
    }
  }
}

void setup() {
  // init Seiral
  Serial.begin(baud_rate);
  ad5761_SPI_init();

  // If Calibrate is needed
  // touch_init();
  // touch_calibrate();

  // init the lvgl interface
  lvgl_control_init();

  // * Create a Task for DAC update * //
  xTaskCreate(
    multitask_dac_update, // task function
    "dac_task", // task name
    2000, // stack size
    NULL, // task parameters
    2, // priority
    NULL // task handle
    );
}

void loop() {
  delay(1);
  // u_int adc_value = 0;
  // while(adc_value < 0xffff){
  //   ad5761_write(CMD_WR_UPDATE_DAC_REG, adc_value, 0);
  //   ad5761_write(CMD_WR_UPDATE_DAC_REG, adc_value, 2);
  //   adc_value += 15;
  // }

  
}

