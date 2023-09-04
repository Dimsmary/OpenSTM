#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "hardware/ad5761.h"
#include "hardware/adda.h"
#include "UartHandle.h"
#include "CommandDistribute.h"

void app_main() {
    // init ad5761(4 Chips)
    ad5761_init();
    // init ad5721 and ads8866
    adda_init();
    // init uart interface
    uarth_init();


    // ad5761_write(CMD_WR_UPDATE_DAC_REG, 32767, 0);
    // adda_ad_write(ADS8689_WRITE_FULL, ADS8689_RANGE_SEL_REG, 0x0000);
    // adda_12bitda_write(CMD_WR_UPDATE_DAC_REG, 0xffff);

    while (1){   
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}