#include "ad5761.h"


// Create spi handle
spi_device_handle_t vspi_handle;

void ad5761_pull_up_ss(char cs){
    // Pull up cs for SPI transmit
    switch (cs)
    {
        case 0:
            gpio_set_level(csPin0, 1);
            break;

        case 1:
            gpio_set_level(csPin1, 1);
            break;

        case 2:
            gpio_set_level(csPin2, 1);
            break;

        case 3:
            gpio_set_level(csPin3, 1);
            break;

        case 4:
            gpio_set_level(csPin0, 1);
            gpio_set_level(csPin1, 1);
            gpio_set_level(csPin2, 1);
            gpio_set_level(csPin3, 1);
            break;
    }
}

void ad5761_pull_down_ss(char cs){
    // Pull up cs for SPI transmit
    switch (cs)
    {
        case 0:
            gpio_set_level(csPin0, 0);
            break;

        case 1:
            gpio_set_level(csPin1, 0);
            break;

        case 2:
            gpio_set_level(csPin2, 0);
            break;

        case 3:
            gpio_set_level(csPin3, 0);
            break;

        case 4:
            gpio_set_level(csPin0, 0);
            gpio_set_level(csPin1, 0);
            gpio_set_level(csPin2, 0);
            gpio_set_level(csPin3, 0);
            break;
    }
}

// init the module
void ad5761_init(){
    ad5761_SPI_init();
    gpio_set_direction(csPin0, GPIO_MODE_OUTPUT);
    gpio_set_direction(csPin1, GPIO_MODE_OUTPUT);
    gpio_set_direction(csPin2, GPIO_MODE_OUTPUT);
    gpio_set_direction(csPin3, GPIO_MODE_OUTPUT);

    ad5761_write(CMD_SW_FULL_RESET,0,0);
    ad5761_write(CMD_WR_CTRL_REG, CONTROL_REG_VAL, 0);
    ad5761_write(CMD_SW_FULL_RESET,0,1);
    ad5761_write(CMD_WR_CTRL_REG, CONTROL_REG_VAL, 1);
    ad5761_write(CMD_SW_FULL_RESET,0,2);
    ad5761_write(CMD_WR_CTRL_REG, CONTROL_REG_VAL, 2);
    ad5761_write(CMD_SW_FULL_RESET,0,3);
    ad5761_write(CMD_WR_CTRL_REG, CONTROL_REG_VAL, 3);

    ad5761_write(CMD_WR_UPDATE_DAC_REG, 32768, 0);
    ad5761_write(CMD_WR_UPDATE_DAC_REG, 32768, 1);
    ad5761_write(CMD_WR_UPDATE_DAC_REG, 32768, 2);
    ad5761_write(CMD_WR_UPDATE_DAC_REG, 32768, 3);

    // All Stand by
    ad5761_pull_up_ss(4);


}

// SPI peripherals initilization
void ad5761_SPI_init(){
    // Create parameters structure
    spi_bus_config_t buscfg={
        .miso_io_num = -1,
        .mosi_io_num = AD5761_MOSI_PIN,
        .sclk_io_num = AD5761_CLK_PIN,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 32,
    };

    // Initilize the spi0
    spi_bus_initialize(AD5761_USED_SPI, &buscfg, SPI_DMA_CH_AUTO);
    spi_device_interface_config_t devcfg0={
        .clock_speed_hz = AD5761_CLOCK_RATE,  
        .mode = 2,                  //SPI mode 0
        .spics_io_num = -1,     
        .queue_size = 1,
        .flags = SPI_DEVICE_HALFDUPLEX,
        .pre_cb = NULL,
        .post_cb = NULL,
    };

    // add SPI device, and return a handle
    spi_bus_add_device(AD5761_USED_SPI, &devcfg0, &vspi_handle);

}

void ad5761_write(uint8_t reg_addr_cmd, uint16_t reg_data, char cs){

    // pull down selected cs
    ad5761_pull_down_ss(cs);

    // Prepare SPI data
    uint8_t tx_data[3];

    tx_data[0] = reg_addr_cmd;
    tx_data[1] = (reg_data & 0xFF00) >> 8;
    tx_data[2] = (reg_data & 0x00FF) >> 0;

    spi_transaction_t t = {
        .tx_buffer = tx_data,
        .length = 3 * 8
    };

    // Transmit SPI data
    spi_device_polling_transmit(vspi_handle, &t);

    // pull up seleted cs
    ad5761_pull_up_ss(cs);
}

