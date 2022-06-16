/*
  ADC_ads8689.h - Header for interfaceing with ads8689 ADC
  Library written by Helmuth Naumer, 2017
  Released under MIT License
*/

/*
Definitions relating to ads8689 ADC
*/

#ifndef ads8689
#define ads8689

// Register Locations and Names
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
#define ADS8689_WRITE_FULL  0b1101000
#define ADS8689_WRITE_MS    0b1101001
#define ADS8689_WRITE_LS    0b1101010
#define ADS8689_SET_HWORD   0b1101100


class ADC_ads8689
{
  public:
    ADC_ads8689(uint8_t buffer_size,uint8_t cs_pin);
    void transmit(uint8_t command,uint16_t address, uint16_t data);
    uint32_t readBuffer(void);
    uint8_t inputAvailable(void);
    void clearBuffer(void);
  private:
    uint32_t* _receive_buffer;
    uint8_t _buffer_size;
    uint8_t _buffer_store_num;
    uint32_t _tmp;
    uint8_t _transmit_bytes[4];
    uint8_t _cs_pin;
};

#endif
