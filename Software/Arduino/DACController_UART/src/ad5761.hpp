// Reference: https://github.com/hellange/AD5761

#ifndef AD5761_H
#define AD5761_H
#include <Arduino.h>
#include <SPI.h>

#define ssPin0  26
#define ssPin1  25
#define ssPin2  33
#define ssPin3  32 

/* Input Shift Register Commands */
#define CMD_NOP                 0x0
#define CMD_WR_TO_INPUT_REG     0x1
#define CMD_UPDATE_DAC_REG      0x2
#define CMD_WR_UPDATE_DAC_REG   0x3
#define CMD_WR_CTRL_REG         0x4
#define CMD_NOP_ALT_1           0x5
#define CMD_NOP_ALT_2           0x6
#define CMD_SW_DATA_RESET       0x7
#define CMD_RESERVED            0x8
#define CMD_DIS_DAISY_CHAIN     0x9
#define CMD_RD_INPUT_REG        0xA
#define CMD_RD_DAC_REG          0xB
#define CMD_RD_CTRL_REG         0xC
#define CMD_NOP_ALT_3           0xD
#define CMD_NOP_ALT_4           0xE
#define CMD_SW_FULL_RESET       0xF



void ad5761_write(uint8_t reg_addr_cmd, uint16_t reg_data, int cs);
void ad5761_read(uint8_t reg_addr_cmd);
void ad5761_print();
void ad5761_SPI_init();
void ad5761_reset();


#endif