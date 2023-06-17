// Reference: https://github.com/hellange/AD5761

#ifndef ad5761_h
#define ad5761_h

#include "driver/spi_master.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "register.h"

// select SPI peripherals
#define AD5761_USED_SPI    SPI3_HOST

// select GPIO pins to used as SPI
#define AD5761_MOSI_PIN            23
#define AD5761_CLK_PIN             18

// define clock rate
#define AD5761_CLOCK_RATE 50000000

// define CS slect
#define csPin0  33
#define csPin1  25
#define csPin2  26
#define csPin3  27

void ad5761_pull_up_ss(char cs);
void ad5761_pull_down_ss(char cs);
void ad5761_init();
void ad5761_SPI_init();
void ad5761_write(uint8_t reg_addr_cmd, uint16_t reg_data, char cs);

#endif