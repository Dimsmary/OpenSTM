// Reference: https://github.com/hellange/AD5761

#include "ad5761.hpp"

byte SPI_Buff[3];


// init SPI interface
void ad5761_SPI_init(){
    pinMode(ssPin0, OUTPUT);  // Set the SS0 pin as an output
    pinMode(ssPin1, OUTPUT);  // Set the SS1 pin as an output

    digitalWrite(ssPin0, LOW);  // Set the SS pin HIGH
    digitalWrite(ssPin1, LOW);
    SPI.begin();  // Begin SPI hardware
    SPI.setClockDivider(SPI_CLOCK_DIV64);  // Slow down SPI clock
    SPI.setDataMode(SPI_MODE2);

    delay(100);

    for(int i = 0; i < 4; i++){
        // AD5761 software reset
        ad5761_write(CMD_SW_FULL_RESET, 0, i);
        // Set the Mode of AD5761
        ad5761_write(CMD_WR_CTRL_REG, 0b0000000101000, i);
    }
   
}

void ad5761_cs_switch(int chip_num){
    delay(1);
    switch(chip_num){
        case 0:
        // clear the low state of target chip
        digitalWrite(ssPin0, HIGH);
        digitalWrite(ssPin1, HIGH);
        delay(1);
        digitalWrite(ssPin0, LOW);
        digitalWrite(ssPin1, LOW);
        break;

        case 1:
        digitalWrite(ssPin0, HIGH);
        digitalWrite(ssPin1, HIGH);
        delay(1);
        digitalWrite(ssPin0, HIGH);
        digitalWrite(ssPin1, LOW);

        break;

        case 2:
        digitalWrite(ssPin0, HIGH);
        digitalWrite(ssPin1, HIGH);
        delay(1);
        digitalWrite(ssPin0, LOW);
        digitalWrite(ssPin1, HIGH);

        break;

        case 3:
        digitalWrite(ssPin0, LOW);
        digitalWrite(ssPin1, LOW);
        delay(1);
        digitalWrite(ssPin0, HIGH);
        digitalWrite(ssPin1, HIGH);
        break;

        default:
        digitalWrite(ssPin0, LOW);
        digitalWrite(ssPin1, LOW);
    }
    delay(1);
}

// SPI Manputaion
void ad5761_write(uint8_t reg_addr_cmd, uint16_t reg_data, int cs){
    uint8_t data[3];
    ad5761_cs_switch(cs);
    data[0] = reg_addr_cmd;
    data[1] = (reg_data & 0xFF00) >> 8;
    data[2] = (reg_data & 0x00FF) >> 0;
    for (int i=0; i<3; i++)
    {
        SPI.transfer(data[i]);
    }

}

void ad5761_read(uint8_t reg_addr_cmd){

    SPI_Buff[0] = SPI.transfer(reg_addr_cmd);
    SPI_Buff[1] = SPI.transfer(0xFF); // dummy
    SPI_Buff[2] = SPI.transfer(0xFF); // dummy

}

// Test Print function
void ad5761_print() {
    Serial.print("CMD:");
    Serial.print(SPI_Buff[0], HEX);
    
    Serial.print(" DATA:");
    Serial.print(SPI_Buff[1], HEX);
    Serial.print(" ");

    Serial.println(SPI_Buff[2], HEX);
}

