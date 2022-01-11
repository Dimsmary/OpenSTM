// from TFT_eSPI/examples/Generic/Touch_calibrate/Touch_calibrate.ino

#ifndef TOUCH_CAL_HPP
#define TOUCH_CAL_HPP
#define TOUCH_CAL 0


#if TOUCH_CAL

#include <Arduino.h>
#include <TFT_eSPI.h>
void touch_init();
void touch_calibrate();
#endif


#endif