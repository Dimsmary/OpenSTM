// Reference: https://github.com/Helmuthn/ads8689_Arduino
// Reference: https://github.com/paulvha/AD57xx

#ifndef adda_h
#define adda_h

#include "driver/spi_master.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "register.h"
#include "uarthandle.h"

// select GPIO pins to used as SPI
#define ADDA_MOSI_PIN   13
#define ADDA_MISO_PIN   12
#define ADDA_CLK_PIN    14
#define DA_CS_PIN       32
#define AD_CS_PIN       4   

// select SPI peripherals
#define ADDA_USED_SPI    SPI2_HOST

// define clock rate
#define ADDA_CLOCK_RATE_AD 20000000
#define ADDA_CLOCK_RATE_DA 40000000

void adda_SPI_init();
void adda_init();
int adda_ad_write(uint8_t command, uint16_t address, uint16_t data);
void adda_12bitda_write(uint8_t reg_addr_cmd, uint16_t reg_data);


#endif