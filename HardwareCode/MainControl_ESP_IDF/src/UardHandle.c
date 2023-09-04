#include "UartHandle.h"

QueueHandle_t tx_quene_A;
// QueueHandle_t tx_quene_B;
bool uart_send_handle_sta = true;

void uarth_init(){
    // Configration for uart
    const uart_config_t uart_config = {
        .baud_rate = BAUD_RATE,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };

    // init the distribution module
    commandD_init();

    // init the uart
    uart_driver_install(UART, RX_BUF_SIZE * 2, 0, 0, NULL, 0);
    uart_param_config(UART, &uart_config);
    uart_set_pin(UART, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    
    // Create the task
    xTaskCreatePinnedToCore(uarth_rx_task, "uart_rx_task", 1024*2, NULL, configMAX_PRIORITIES - PRIORITY_RX, NULL, CORE_RX);
    xTaskCreatePinnedToCore(uarth_tx_task, "uart_tx_task", 1024*2, NULL, configMAX_PRIORITIES - PRIORITY_TX, NULL, CORE_TX);
}


void uarth_tx_task(void *arg){
    // Create a buffer to receive queue data
    char txBuffer[TX_SINGLE_SIZE];

    // Create the quene
    tx_quene_A = xQueueCreate(TX_QUENE_LENGTH, sizeof(txBuffer));
    while (1) {
        if(xQueueReceive(tx_quene_A, &(txBuffer), portMAX_DELAY)){
        uart_write_bytes(UART, txBuffer, strlen(txBuffer));
        }
    }
}

void uarth_rx_task(void *arg){
    // Buffer to load the receive data from uart
    uint8_t* data = (uint8_t*) malloc(RX_BUF_SIZE+1);

    while (1) {
        const int rxBytes = uart_read_bytes(UART, data, 12, 10 / portTICK_PERIOD_MS);
        if (rxBytes > 0) {
            data[rxBytes] = 0;

            // load first 10 character
            char command[10];
            strncpy(command, (char*) data, sizeof(command));

            // send the data to command distribute task
            // xQueueSend(tx_quene, command, (TickType_t)0);
            xQueueSend(command_distribute_quene, command, 0 / portTICK_PERIOD_MS);


            // dump the rest of the serial data
        }
    }
    free(data);
}


