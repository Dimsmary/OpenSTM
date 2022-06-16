#ifndef CONTROL_HPP
#define CONTROL_HPP
#include <Arduino.h>
#include "ad5761.hpp"
#include "ads868x.hpp"
#include "steppermotor.hpp"
#include "uartcommand.hpp"


#define SAM_DAC   0
#define Z_DAC     1
#define Y_DAC     2
#define X_DAC     3

extern uartcommand UartCommand;
extern ADC_ads868x ads868x;

class controlflow
{
    public:
    // Scanning Parameters
    int scan_mode;

    // Store the register of DAC
    int dac_register_x;
    int dac_register_y;
    int dac_register_z;
    int dac_register_sample;

    // Fine Approach mode prameters
    uint16_t tunneling_voltage_limit;
    uint16_t drawback_voltage_limit;
    uint16_t forward_step;
    bool tunneling_established;
    bool command_est_send;
    bool command_crash_send;
    uint16_t z_step;
    uint16_t z_delay_time;
    bool z_scan;
    uint16_t piezo_drwaback;
    uint16_t z_test_step;
    uint16_t z_test_delay_time;

    // bias test parameters
    uint16_t bias_end;
    uint16_t bias_step;
    bool is_bias_test;

    // Scanning parameters
    uint16_t x_max_range;
    uint16_t x_min_range;
    uint16_t y_max_range;
    uint16_t y_min_range;
    uint16_t xy_step;
    uint16_t xy_delay_time;
    bool x_forward;
    bool y_forward;
    bool scan_finished;
    bool xy_reverse;

    controlflow();
    void update();
    void all_status_reset();

};



#endif