#include <Arduino.h>
#ifndef MOTORCONTROL_HPP
#define MOTORCONTROL_HPP


int phaseForward(int phase);
int phaseBackward(int phase);
void motorGPIOSetup(int motor[]);
void switchPhase(int motor[], int phase);


#endif