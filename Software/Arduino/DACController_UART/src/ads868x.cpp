// REF: https://github.com/Helmuthn/ads8689_Arduino

#include "ads868x.hpp"

/*
  Initialize the object to be used.
  Create a buffer of size buffer_size, and select the pin connected to cs.
*/
ADC_ads868x::ADC_ads868x(uint8_t buffer_size)
{
  uint32_t receive_buffer[buffer_size];
  _receive_buffer = receive_buffer;
  _buffer_store_num = 0;
  _buffer_size = buffer_size;
  _cs_pin = CS_PIN;

  pinMode(CS_PIN, OUTPUT);
  SPI1 = SPIClass(HSPI);
  SPI1.begin();
  SPI1.setClockDivider(SPI_CLOCK_DIV2);
  reset();
}

/*
  Transmit a properly formatted message.
  Provide the command (from the headers), the address associated with it,
  and the 16 bits of data.

  See the header and datasheet for the list of commands and memory locations.
*/
void ADC_ads868x::transmit(uint8_t command, uint16_t address, uint16_t data)
{ 
  if(_buffer_size > _buffer_store_num){
    _receive_buffer[_buffer_store_num] = 0;
    _transmit_bytes[0] = (command<<1)|((address>>8)&1);
    _transmit_bytes[1] = (address&0xFF);
    _transmit_bytes[2] = ((data>>8)&0xFF);
    _transmit_bytes[3] = (data&0xFF);
    uint8_t i = 0;
    digitalWrite(_cs_pin,LOW);
    SPI1.beginTransaction(SPISettings(100000, MSBFIRST, SPI_MODE0));
    SPI1.transfer(_transmit_bytes,4);
    SPI1.endTransaction();
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
uint32_t ADC_ads868x::readBuffer(void)
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
uint8_t ADC_ads868x::inputAvailable(void)
{
  return _buffer_store_num;
}

/*
  Clears the buffer.
*/
void ADC_ads868x::clearBuffer(){
  _buffer_store_num = 0;
}

uint16_t ADC_ads868x::readADC(void){
  transmit(ADS8689_NOP, 0, 0);
  uint32_t read_adc = readBuffer();
  uint16_t read_adc_high = (read_adc >> 16) & 0x0000FFFF;
  return read_adc_high;
}

void ADC_ads868x::reset(void){
  transmit(ADS8689_WRITE_FULL, ADS8689_RANGE_SEL_REG, 0x0000);
}