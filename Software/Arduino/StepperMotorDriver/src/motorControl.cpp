#include "motorControl.hpp"


int phaseForward(int phase){
  if (phase < 7){
    phase ++;
  }
  else{
    phase = 0;
  }
  return phase;
}

int phaseBackward(int phase){
  if(phase > 0){
    phase --;
  }
  else{
    phase = 7;
  }
  return phase;
}

// setting up the GPIO
void motorGPIOSetup(int motor[]){
  for(int i = 0; i < 4; i++){
    pinMode(motor[i], OUTPUT);
    digitalWrite(motor[i], LOW);
  }
}

// change the phase of stepper motor(half-step with 8 phase total)
void switchPhase(int motor[], int phase){
  switch(phase){
    case 0:
      digitalWrite(motor[0], HIGH);
      digitalWrite(motor[1], LOW);
      digitalWrite(motor[2], LOW);
      digitalWrite(motor[3], LOW);
      break;
    case 1:
      digitalWrite(motor[0], HIGH);
      digitalWrite(motor[1], HIGH);
      digitalWrite(motor[2], LOW);
      digitalWrite(motor[3], LOW);
      break;
    case 2:
      digitalWrite(motor[0], LOW);
      digitalWrite(motor[1], HIGH);
      digitalWrite(motor[2], LOW);
      digitalWrite(motor[3], LOW);
      break;
    case 3:
      digitalWrite(motor[0], LOW);
      digitalWrite(motor[1], HIGH);
      digitalWrite(motor[2], HIGH);
      digitalWrite(motor[3], LOW);
      break;
    case 4:
      digitalWrite(motor[0], LOW);
      digitalWrite(motor[1], LOW);
      digitalWrite(motor[2], HIGH);
      digitalWrite(motor[3], LOW);
      break;
    case 5:
      digitalWrite(motor[0], LOW);
      digitalWrite(motor[1], LOW);
      digitalWrite(motor[2], HIGH);
      digitalWrite(motor[3], HIGH);
      break;
    case 6:
      digitalWrite(motor[0], LOW);
      digitalWrite(motor[1], LOW);
      digitalWrite(motor[2], LOW);
      digitalWrite(motor[3], HIGH);
      break;
    case 7:
      digitalWrite(motor[0], HIGH);
      digitalWrite(motor[1], LOW);
      digitalWrite(motor[2], LOW);
      digitalWrite(motor[3], HIGH);
      break;
    case 8:
    digitalWrite(motor[0], LOW);
    digitalWrite(motor[1], LOW);
    digitalWrite(motor[2], LOW);
    digitalWrite(motor[3], LOW);
    break;
  }
}