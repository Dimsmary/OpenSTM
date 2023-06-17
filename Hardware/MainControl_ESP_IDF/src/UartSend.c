#include "UartSend.h"
bool uart_send_sta = true;


void UARTS_write(char* data){
    // Prepare for the data
    char dataLRLN[UART_QUENE_BUFFER_SIZE];
    strncpy(dataLRLN, data, sizeof(dataLRLN));
    strcat(dataLRLN, "\r\n");
    
    // send data to the buffer
    xQueueSend(tx_quene_A, dataLRLN, (TickType_t)1000);
    
}

