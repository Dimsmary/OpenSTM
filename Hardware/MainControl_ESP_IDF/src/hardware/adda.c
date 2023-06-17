#include "adda.h"


// Create spi handle
spi_device_handle_t hspi_handle_ad;
spi_device_handle_t hspi_handle_da;

void adda_init(){
    adda_SPI_init();

    // ads8685 init
    // reset
    adda_ad_write(ADS8689_WRITE_FULL, ADS8689_RST_PWRCTL_REG, 0);
    // set range to +-2.56
    adda_ad_write(ADS8689_WRITE_FULL, ADS8689_RANGE_SEL_REG, 4);
    

    // ad5721 init
    adda_12bitda_write(CMD_SW_FULL_RESET, 0);
    adda_12bitda_write(CMD_WR_CTRL_REG, CONTROL_REG_VAL_R);

}

void adda_ad_reset(uint16_t REG){
    // reset
    adda_ad_write(ADS8689_WRITE_FULL, ADS8689_RST_PWRCTL_REG, 0);
    // set range to +-2.56
    adda_ad_write(ADS8689_WRITE_FULL, REG, 4);
}

// SPI peripherals initilization
void adda_SPI_init(){
    // Create parameters structure
    spi_bus_config_t buscfg={
        .miso_io_num = ADDA_MISO_PIN,
        .mosi_io_num = ADDA_MOSI_PIN,
        .sclk_io_num = ADDA_CLK_PIN,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 32,
    };

    // Initilize the spi0
    spi_bus_initialize(ADDA_USED_SPI, &buscfg, SPI_DMA_CH_AUTO);

    // add device
    spi_device_interface_config_t devcfg_ad={
        .clock_speed_hz = ADDA_CLOCK_RATE_AD,  
        .mode = 0,                  //SPI mode 0
        .spics_io_num = AD_CS_PIN,     
        .queue_size = 1,
        // .flags = SPI_DEVICE_HALFDUPLEX,
        .pre_cb = NULL,
        .post_cb = NULL,
    };

    spi_device_interface_config_t devcfg_da={
        .clock_speed_hz = ADDA_CLOCK_RATE_DA,  
        .mode = 2,                  //SPI mode 2
        .spics_io_num = DA_CS_PIN,     
        .queue_size = 1,
        .flags = SPI_DEVICE_HALFDUPLEX,
        .pre_cb = NULL,
        .post_cb = NULL,
    };

    // add SPI device, and return a handle
    spi_bus_add_device(ADDA_USED_SPI, &devcfg_ad, &hspi_handle_ad);
    spi_bus_add_device(ADDA_USED_SPI, &devcfg_da, &hspi_handle_da);
}

int adda_ad_write(uint8_t command, uint16_t address, uint16_t data){
    // prepare for adc send data
    uint8_t transmit_bytes[4];
    transmit_bytes[0] = (command<<1)|((address>>8)&1);
    transmit_bytes[1] = (address&0xFF);
    transmit_bytes[2] = ((data>>8)&0xFF);
    transmit_bytes[3] = (data&0xFF);

    // create struct for transmit
    spi_transaction_t t = {
        .tx_buffer = transmit_bytes,
        .length = 4 * 8,
        .rxlength = 4 * 8,
        .flags = SPI_TRANS_USE_RXDATA
    };


    // get adc data
    spi_device_polling_transmit(hspi_handle_ad, &t);

    // process the data
    int receive_data = 0;
    receive_data = receive_data | t.rx_data[0];
    receive_data = receive_data << 8;
    receive_data = receive_data | t.rx_data[1];
    
    return receive_data;
}


void adda_12bitda_write(uint8_t reg_addr_cmd, uint16_t reg_data){
    // Prepare SPI data
    uint8_t tx_data[3];

    // for mat the data
    tx_data[0] = reg_addr_cmd;
    tx_data[1] = (reg_data & 0xFF00) >> 8;
    tx_data[2] = (reg_data & 0x00FF) >> 0;

    // prepare for spi data structure
    spi_transaction_t t = {
        .tx_buffer = tx_data,
        .length = 3 * 8
    };

    // send data
    spi_device_polling_transmit(hspi_handle_da, &t);
}





