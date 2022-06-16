#ifndef STEPPERMOTOR_HPP
#define STEPPERMOTOR_HPP
#include <Arduino.h>

#define MOTORA_STOP         "AS"
#define MOTORB_STOP         "BS"
#define MOTORC_STOP         "CS"
#define MOTORA_BEGIN        "AG"
#define MOTORA_BEGIN_B      "AG1"
#define MOTORB_BEGIN        "BG"
#define MOTORB_BEGIN_B      "BG1"
#define MOTORC_BEGIN        "CG"
#define MOTORC_BEGIN_B      "CG1"
#define MOTORA_STEPFORWARD  "AF"
#define MOTORA_STEPBACKWARD "AB"
#define MOTORB_STEPFORWARD  "BF"
#define MOTORB_STEPBACKWARD "BB"
#define MOTORC_STEPFORWARD  "CF"
#define MOTORC_STEPBACKWARD "CB"
#define MOTORA_RELEASE      "AR"
#define MOTORB_RELEASE      "BR"
#define MOTORC_RELEASE      "CR"
#define SET_DELAY_TIME      "SP"


void stepper_init(int baud_rate);
void stepper_set_delay(int delay_time);
void stepper_fine_forward(int loop_times);
void stepper_fine_backward(int loop_times);
void stepper_coarse_approach(bool begin, bool forward);
void stepper_coarse_single(int num, bool forward);
void stepper_release(int num);


#endif