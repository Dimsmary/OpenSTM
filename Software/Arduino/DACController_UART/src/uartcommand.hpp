#ifndef UARTCOMMAND_HPP
#define UARTCOMMAND_HPP
#include <Arduino.h>

#define COMMAND_ADC     "AD"
#define COMMAND_DAC_X   "DX"
#define COMMAND_DAC_Y   "DY"
#define COMMAND_DAC_Z   "DZ"
#define COMMAND_DAC_SAMPLE   "DS"


class uartcommand
{
private:
    String command;
    int head_num;
    String header;
    int param;
    bool is_command;
    
public:
    uartcommand(int baud_rate, int header_num);
    void read_uart();
    bool is_command_finished();
    String get_header();
    int get_param();

    void upload_adc(uint16_t register_value);
    void upload_dac_x(uint16_t register_value);
    void upload_dac_y(uint16_t register_value);
    void upload_dac_z(uint16_t register_value);
    void upload_dac_sample(uint16_t register_value);
    void return_ok();
};


#endif