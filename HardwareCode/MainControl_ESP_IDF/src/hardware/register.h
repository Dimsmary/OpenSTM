#ifndef REGISTER_H
#define REGISTER_H

/* Input Shift Register Commands for AD57X1 */
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


// Control Reg Settings
// XXXXX-XX-X-X-X-X-XX-XXX
// 00000 (DONT' CARE)
// 00    (CLEAR Voltage select: 00 Zero, 01 Mid, 10/11 Full)
// 0     (Over Range: 0 Disable, 1 5%OverRange)
// 0     (Bipolar Range: 0 BinaryCode, 1 Twos complement coded)
// 1     (Thermal shutdown(150C powerdown): 0 Disable, 1 Enable)
// 0     (DB5)
// 01    (Power Up Voltage: 00: Zero, 01 Mid, 10/11 Full)
// 000   (Output Range: 000 -10~+10, 001 0~+10, 010 -5~+5, 011 )
#define CONTROL_REG_VAL 0b0000000001001000
// With Reference Version
#define CONTROL_REG_VAL_R 0b0000000001101000

/* Input Shift Register Commands for ADS8689 */
#define ADS8689_DEVICE_ID_REG   0x00
#define ADS8689_RST_PWRCTL_REG  0x04
#define ADS8689_SDI_CTL_REG     0x08
#define ADS8689_SDO_CTL_REG     0x0C
#define ADS8689_DATAOUT_CTL_REG 0x10
#define ADS8689_RANGE_SEL_REG   0x14
#define ADS8689_ALARM_REG       0x20
#define ADS8689_ALARM_H_TH_REG  0x24
#define ADS8689_ALARM_L_TH_REG  0x28

// SPI commands
#define ADS8689_NOP         0b0000000
#define ADS8689_CLEAR_HWORD 0b1100000
#define ADS8689_READ_HWORD  0b1100100
#define ADS8689_READ        0b0100100
#define ADS8689_WRITE_FULL  0b1101000 //write 16 bits to register
#define ADS8689_WRITE_MS    0b1101001
#define ADS8689_WRITE_LS    0b1101010

#endif