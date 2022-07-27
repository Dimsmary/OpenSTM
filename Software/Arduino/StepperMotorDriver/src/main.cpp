#include <Arduino.h>
#include "motorControl.hpp"

// define your GPIO used here
#define B0 13
#define C0 14
#define D0 15
#define E0 19
#define B1 18
#define C1 17
#define D1 16
#define E1 5
#define B2 6
#define C2 7
#define D2 8
#define E2 9


// define GPIO set of stepper motor
int motorA[4] = {B0, C0, D0, E0};
int motorB[4] = {B1, C1, D1, E1};
int motorC[4] = {B2, C2, D2, E2};

// Motor phase storage
int phaseA = 0;
int phaseB = 0;
int phaseC = 0;

// Motor status storage
bool motorA_begin = false;
bool motorB_begin = false;
bool motorC_begin = false;

bool motorA_forward = false;
bool motorB_forward = false;
bool motorC_forward = false;

// Motor speed storage
int delay_time = 10;

// uart command receive
bool stringComplete = false;
String command = "";


void setup() {
  // setting up the GPIO
  motorGPIOSetup(motorA);
  motorGPIOSetup(motorB);
  motorGPIOSetup(motorC);

  // setting up the uart
  Serial.begin(9600);
}

void loop() {
  //** UART COMMAND **//
  // read command
  if (Serial.available()) {
    char singleChar;
    singleChar = Serial.read();
    command += singleChar;
    if(singleChar == 10){
      stringComplete = true;
    }
  }


  // if command receive completed
  if(stringComplete){
    // devide command into head and param
    String command_head = command.substring(0,2);
    int command_param= command.substring(2, command.length()).toInt();
    if(command_head == "SP"){
      delay_time = command_param;
      Serial.print("Speed Set:");
      Serial.println(delay_time);
    }

    // MotorA
    else if(command_head == "AF"){
      Serial.println("Motor A StepForwad 1.");
      phaseA = phaseForward(phaseA);
    }
    else if(command_head == "AB"){
      Serial.println("Motor A StepBackward 1.");
      phaseA = phaseBackward(phaseA);
    }
    else if(command_head == "AG"){
      Serial.println("Motor A Go.");
      if(command_param == 0){
        motorA_forward = true;
      }
      else{
        motorA_forward = false;
      }
      motorA_begin = true;
    }
    else if(command_head == "AS"){
      Serial.println("Motor A Stop.");
      motorA_begin = false;
    }

    else if(command_head == "AR"){
      Serial.println("Motor A Released.");
      motorA_begin = false;
      switchPhase(motorA, 8);
      phaseA = 8;
    }

    // MotorB
    else if(command_head == "BF"){
      Serial.println("Motor B StepForwad 1.");
      phaseB = phaseForward(phaseB);
    }
    else if(command_head == "BB"){
      Serial.println("Motor B StepBackward 1.");
      phaseB = phaseBackward(phaseB);
    }
    else if(command_head == "BG"){
      Serial.println("Motor B Go.");
      if(command_param == 0){
        motorB_forward = true;
      }
      else{
        motorB_forward = false;
      }
      motorB_begin = true;
    }
    else if(command_head == "BS"){
      Serial.println("Motor B Stop.");
      motorB_begin = false;
    }

    else if(command_head == "BR"){
      Serial.println("Motor B Released.");
      motorB_begin = false;
      phaseB = 8;
    }

    // MotorC
    else if(command_head == "CF"){
      Serial.println("Motor C StepForwad 1.");
      phaseC = phaseForward(phaseC);
    }
    else if(command_head == "CB"){
      Serial.println("Motor C StepBackward 1.");
      phaseC = phaseBackward(phaseC);
    }
    else if(command_head == "CG"){
      Serial.println("Motor C Go.");
      if(command_param == 0){
        motorC_forward = true;
      }
      else{
        motorC_forward = false;
      }
      motorC_begin = true;
    }
    else if(command_head == "CS"){
      Serial.println("Motor C Stop.");
      motorC_begin = false;
    }

    else if(command_head == "CR"){
      Serial.println("Motor C Released.");
      motorC_begin = false;
      phaseC = 8;
    }


    command = "";
    stringComplete = false;
  }

  //** LOOP CONTROL **//
  if(motorA_begin){
    if(motorA_forward){
      phaseA = phaseForward(phaseA);
    }
    else{
      phaseA = phaseBackward(phaseA);
    }
  }

  if(motorB_begin){
    if(motorB_forward){
      phaseB = phaseForward(phaseB);
    }
    else{
      phaseB = phaseBackward(phaseB);
    }
  }

  if(motorC_begin){
    if(motorC_forward){
      phaseC = phaseForward(phaseC);
    }
    else{
      phaseC = phaseBackward(phaseC);
    }
  }

  
  switchPhase(motorA, phaseA);
  switchPhase(motorB, phaseB);
  switchPhase(motorC, phaseC);

  delay(delay_time);
}