#include "steppermotor.hpp"

void stepper_init(int baud_rate){
    Serial2.begin(baud_rate);
    Serial2.println(MOTORA_STOP);
    Serial2.println(MOTORB_STOP);
    Serial2.println(MOTORC_STOP);
}


// *** SET DELAY TIME *** //
void stepper_set_delay(int delay_time){
    Serial2.println(SET_DELAY_TIME + String(delay_time));
}


// *** Coarse Approach *** //
void stepper_coarse_approach(bool begin, bool forward){
    if(begin){
        if(forward){
            Serial2.println(MOTORA_BEGIN);
            Serial2.println(MOTORB_BEGIN);
            Serial2.println(MOTORC_BEGIN);
        }
        else{
            Serial2.println(MOTORA_BEGIN_B);
            Serial2.println(MOTORB_BEGIN_B);
            Serial2.println(MOTORC_BEGIN_B);
        }
        
    }
    else{
        Serial2.println(MOTORA_STOP);
        Serial2.println(MOTORB_STOP);
        Serial2.println(MOTORC_STOP);
    }
}

void stepper_coarse_single(int num, bool forward){
    switch (num)
    {
    case 1:
        if(forward){
            Serial2.println(MOTORA_BEGIN);
        }else{
            Serial2.println(MOTORA_BEGIN_B);
        }
        break;
    
    case 2:
        if(forward){
            Serial2.println(MOTORB_BEGIN);
        }else{
            Serial2.println(MOTORB_BEGIN_B);
        }
        break;

    case 3:
        if(forward){
            Serial2.println(MOTORC_BEGIN);
        }else{
            Serial2.println(MOTORC_BEGIN_B);
        }
        break;
    }
}


// *** Fine Approach *** //
void stepper_fine_forward(int loop_times){
    for(int i = 0; i < loop_times; i++){
        Serial2.println(MOTORA_STEPFORWARD);
    }
}

void stepper_fine_backward(int loop_times){
    for(int i = 0; i < loop_times; i++){
        Serial2.println(MOTORA_STEPBACKWARD);
    }
}

void stepper_release(int num){
    switch(num){
        case 0:
        Serial2.println(MOTORA_RELEASE);
        break;
        
        case 1:
        Serial2.println(MOTORB_RELEASE);
        break;

        case 2:
        Serial2.println(MOTORC_RELEASE);
        break;

        default:
        break;
    }
}