#include "uartcommand.hpp"


uartcommand::uartcommand(int baud_rate, int header_num)
{
    Serial.begin(baud_rate);
    command = "";
    head_num = header_num;
    is_command = false;
}

void uartcommand::read_uart(){
    // receive command
    if (Serial.available()) {
        char singleChar;
        singleChar = Serial.read();
        command += singleChar;
        if(singleChar == 10){
            // decode the command
            header = command.substring(0,head_num);
            param = command.substring(head_num, command.length()).toInt();
            // empty the command
            is_command = true;
            command = "";
        }
    }
}


// return command receive status
bool uartcommand::is_command_finished(){
    return is_command;
}

String uartcommand::get_header(){
    is_command = false;
    return header;
}

int uartcommand::get_param(){
    is_command = false;
    return param;
}

// upload command
void uartcommand::upload_adc(uint16_t register_value){
    Serial.println(COMMAND_ADC + String(register_value));
}

void uartcommand::upload_dac_x(uint16_t register_value){
    Serial.println(COMMAND_DAC_X + String(register_value));
}

void uartcommand::upload_dac_y(uint16_t register_value){
    Serial.println(COMMAND_DAC_Y + String(register_value));
}

void uartcommand::upload_dac_z(uint16_t register_value){
    Serial.println(COMMAND_DAC_Z + String(register_value));
}

void uartcommand::upload_dac_sample(uint16_t register_value){
    Serial.println(COMMAND_DAC_SAMPLE + String(register_value));
}

void uartcommand::return_ok(){
    Serial.println("OK");
}
