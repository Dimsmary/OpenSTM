#ifndef LVGL_CONTROL_APPROACH_HPP
#define LVGL_CONTROL_APPROACH_HPP

#include <Arduino.h>
#include <lvgl.h>

#define REG_COL "#005780"
#define VOL_COL "#800000"
#define ADC_COL "#4bc230"

#define SCAN_FORWARD true
#define SCAN_BACKWARD false


void GUI_init();
int approach_get_z_power();
int approach_get_z_register();
int approach_get_tip_power();
int approach_get_tip_register();


#endif