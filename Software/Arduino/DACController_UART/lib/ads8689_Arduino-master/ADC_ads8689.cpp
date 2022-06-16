/*
  ADC_ads8689.cpp - Library for interfaceing with ads8689 ADC
  Library written by Helmuth Naumer, 2017
  Released under MIT License
*/

#include "Arduino.h"
#include "ADC_ads8689.h"
#include "SPI.h"

/*
  Initialize the object to be used.
  Create a buffer of size buffer_size, and select the pin connected to cs.
*/
ADC_ads8689::ADC_ads8689(uint8_t buffer_size,uint8_t cs_pin)
{
  uint32_t receive_buffer[buffer_size];
  _receive_buffer = receive_buffer;
  _buffer_store_num = 0;
  _buffer_size = buffer_size;
  _cs_pin = cs_pin;
  SPI.begin();

}

/*
  Transmit a properly formatted message.
  Provide the command (from the headers), the address associated with it,
  and the 16 bits of data.

  See the header and datasheet for the list of commands and memory locations.
*/
void ADC_ads8689::transmit(uint8_t command, uint16_t address, uint16_t data)
{ 
  if(_buffer_size > _buffer_store_num){
    _receive_buffer[_buffer_store_num] = 0;
    _transmit_bytes[0] = (command<<1)|((address>>8)&1);
    _transmit_bytes[1] = (address&0xFF);
    _transmit_bytes[2] = ((data>>8)&0xFF);
    _transmit_bytes[3] = (data&0xFF);
    uint8_t i = 0;
    digitalWrite(_cs_pin,LOW);
    SPI.beginTransaction(SPISettings(16000000, MSBFIRST, SPI_MODE0));
    SPI.transfer(_transmit_bytes,4);
    SPI.endTransaction();
    digitalWrite(_cs_pin,HIGH);
    while(i<4){
      _receive_buffer[_buffer_store_num] = (_receive_buffer[_buffer_store_num]<<8);
      _receive_buffer[_buffer_store_num] |= _transmit_bytes[i];
      i++;
    }
    _buffer_store_num++;
  }
}


/*
  Pop a value off of the top of the buffer.
  Buffer acts as a stack.
*/
uint32_t ADC_ads8689::readBuffer(void)
{
  if(_buffer_store_num > 0){
    _buffer_store_num--;
    _tmp = _receive_buffer[_buffer_store_num];
    return _tmp;
  }
  return 0xFFFF;
}

/*
  Returns the number of items in the buffer
*/
uint8_t ADC_ads8689::inputAvailable(void)
{
  return _buffer_store_num;
}

/*
  Clears the buffer.
*/
void ADC_ads8689::clearBuffer(){
  _buffer_store_num = 0;
}
