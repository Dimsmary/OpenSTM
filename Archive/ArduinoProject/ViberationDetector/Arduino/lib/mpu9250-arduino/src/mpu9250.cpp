/*
* Brian R Taylor
* brian.taylor@bolderflight.com
* 
* Copyright (c) 2021 Bolder Flight Systems Inc
*
* Permission is hereby granted, free of charge, to any person obtaining a copy
* of this software and associated documentation files (the “Software”), to
* deal in the Software without restriction, including without limitation the
* rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
* sell copies of the Software, and to permit persons to whom the Software is
* furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
* AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
* IN THE SOFTWARE.
*/

#include "Arduino.h"
#include "Wire.h"
#include "SPI.h"
#include "mpu9250.h"

Mpu9250::Mpu9250(TwoWire *bus, uint8_t addr) {
  iface_ = I2C;
  i2c_ = bus;
  conn_ = addr;
}
Mpu9250::Mpu9250(SPIClass *bus, uint8_t cs) {
  iface_ = SPI;
  spi_ = bus;
  conn_ = cs;
}
bool Mpu9250::Begin() {
  if (iface_ == I2C) {
    i2c_->begin();
    i2c_->setClock(I2C_CLOCK_);
  } else {
    pinMode(conn_, OUTPUT);
    #if defined(__MK20DX128__) || defined(__MK20DX256__) || \
        defined(__MK64FX512__) || defined(__MK66FX1M0__) || \
        defined(__MKL26Z64__)  || defined(__IMXRT1062__) || \
        defined(__IMXRT1052__)
    digitalWriteFast(conn_, HIGH);
    #else
    digitalWrite(conn_, HIGH);
    #endif
    spi_->begin();
  }
  spi_clock_ = 1000000;
  /* Select clock source to gyro */
  if (!WriteRegister(PWR_MGMNT_1_, CLKSEL_PLL_)) {
    return false;
  }
  /* Enable I2C master mode */
  if (!WriteRegister(USER_CTRL_, I2C_MST_EN_)) {
    return false;
  }
  /* Set the I2C bus speed to 400 kHz */
  if (!WriteRegister(I2C_MST_CTRL_, I2C_MST_CLK_)) {
    return false;
  }
  /* Set AK8963 to power down */
  WriteAk8963Register(AK8963_CNTL1_, AK8963_PWR_DOWN_);
  /* Reset the MPU9250 */
  WriteRegister(PWR_MGMNT_1_, H_RESET_);
  /* Wait for MPU-9250 to come back up */
  delay(1);
  /* Reset the AK8963 */
  WriteAk8963Register(AK8963_CNTL2_, AK8963_RESET_);
  /* Select clock source to gyro */
  if (!WriteRegister(PWR_MGMNT_1_, CLKSEL_PLL_)) {
    return false;
  }
  /* Check the WHO AM I byte */
  uint8_t who_am_i;
  if (!ReadRegisters(WHOAMI_, sizeof(who_am_i), &who_am_i)) {
    return false;
  }
  if ((who_am_i != WHOAMI_MPU9250_) && (who_am_i != WHOAMI_MPU9255_)) {
    return false;
  }
  /* Enable I2C master mode */
  if (!WriteRegister(USER_CTRL_, I2C_MST_EN_)) {
    return false;
  }
  /* Set the I2C bus speed to 400 kHz */
  if (!WriteRegister(I2C_MST_CTRL_, I2C_MST_CLK_)) {
    return false;
  }
  /* Check the AK8963 WHOAMI */
  if (!ReadAk8963Registers(AK8963_WHOAMI_, sizeof(who_am_i), &who_am_i)) {
    return false;
  }
  if (who_am_i != WHOAMI_AK8963_) {
    return false;
  }
  /* Get the magnetometer calibration */
  /* Set AK8963 to power down */
  if (!WriteAk8963Register(AK8963_CNTL1_, AK8963_PWR_DOWN_)) {
    return false;
  }
  delay(100);  // long wait between AK8963 mode changes
  /* Set AK8963 to FUSE ROM access */
  if (!WriteAk8963Register(AK8963_CNTL1_, AK8963_FUSE_ROM_)) {
    return false;
  }
  delay(100);  // long wait between AK8963 mode changes
  /* Read the AK8963 ASA registers and compute magnetometer scale factors */
  uint8_t asa_buff[3];
  if (!ReadAk8963Registers(AK8963_ASA_, sizeof(asa_buff), asa_buff)) {
    return false;
  }
  mag_scale_[0] = ((static_cast<float>(asa_buff[0]) - 128.0f)
    / 256.0f + 1.0f) * 4912.0f / 32760.0f;
  mag_scale_[1] = ((static_cast<float>(asa_buff[1]) - 128.0f)
    / 256.0f + 1.0f) * 4912.0f / 32760.0f;
  mag_scale_[2] = ((static_cast<float>(asa_buff[2]) - 128.0f)
    / 256.0f + 1.0f) * 4912.0f / 32760.0f;
  /* Set AK8963 to power down */
  if (!WriteAk8963Register(AK8963_CNTL1_, AK8963_PWR_DOWN_)) {
    return false;
  }
  /* Set AK8963 to 16 bit resolution, 100 Hz update rate */
  if (!WriteAk8963Register(AK8963_CNTL1_, AK8963_CNT_MEAS2_)) {
    return false;
  }
  delay(100);  // long wait between AK8963 mode changes
  /* Select clock source to gyro */
  if (!WriteRegister(PWR_MGMNT_1_, CLKSEL_PLL_)) {
    return false;
  }
  /* Instruct the MPU9250 to get 7 bytes from the AK8963 at the sample rate */
  uint8_t mag_data[7];
  if (!ReadAk8963Registers(AK8963_HXL_, sizeof(mag_data), mag_data)) {
    return false;
  }
  /* Set the accel range to 16G by default */
  if (!ConfigAccelRange(ACCEL_RANGE_16G)) {
    return false;
  }
  /* Set the gyro range to 2000DPS by default*/
  if (!ConfigGyroRange(GYRO_RANGE_2000DPS)) {
    return false;
  }
  /* Set the DLPF to 20HZ by default */
  if (!ConfigDlpf(DLPF_BANDWIDTH_20HZ)) {
    return false;
  }
  /* Set the SRD to 0 by default */
  if (!ConfigSrd(0)) {
    return false;
  }
  return true;
}
bool Mpu9250::EnableDrdyInt() {
  spi_clock_ = 1000000;
  if (!WriteRegister(INT_PIN_CFG_, INT_PULSE_50US_)) {
    return false;
  }
  if (!WriteRegister(INT_ENABLE_, INT_RAW_RDY_EN_)) {
    return false;
  }
  return true;
}
bool Mpu9250::DisableDrdyInt() {
  spi_clock_ = 1000000;
  if (!WriteRegister(INT_ENABLE_, INT_DISABLE_)) {
    return false;
  }
  return true;
}
bool Mpu9250::ConfigAccelRange(const AccelRange range) {
  AccelRange requested_range;
  float requested_scale;
  spi_clock_ = 1000000;
  /* Check input is valid and set requested range and scale */
  switch (range) {
    case ACCEL_RANGE_2G: {
      requested_range = range;
      requested_scale = 2.0f / 32767.5f;
      break;
    }
    case ACCEL_RANGE_4G: {
      requested_range = range;
      requested_scale = 4.0f / 32767.5f;
      break;
    }
    case ACCEL_RANGE_8G: {
      requested_range = range;
      requested_scale = 8.0f / 32767.5f;
      break;
    }
    case ACCEL_RANGE_16G: {
      requested_range = range;
      requested_scale = 16.0f / 32767.5f;
      break;
    }
    default: {
      return false;
    }
  }
  /* Try setting the requested range */
  if (!WriteRegister(ACCEL_CONFIG_, requested_range)) {
    return false;
  }
  /* Update stored range and scale */
  accel_range_ = requested_range;
  accel_scale_ = requested_scale;
  return true;
}
bool Mpu9250::ConfigGyroRange(const GyroRange range) {
  GyroRange requested_range;
  float requested_scale;
  spi_clock_ = 1000000;
  /* Check input is valid and set requested range and scale */
  switch (range) {
    case GYRO_RANGE_250DPS: {
      requested_range = range;
      requested_scale = 250.0f / 32767.5f;
      break;
    }
    case GYRO_RANGE_500DPS: {
      requested_range = range;
      requested_scale = 500.0f / 32767.5f;
      break;
    }
    case GYRO_RANGE_1000DPS: {
      requested_range = range;
      requested_scale = 1000.0f / 32767.5f;
      break;
    }
    case GYRO_RANGE_2000DPS: {
      requested_range = range;
      requested_scale = 2000.0f / 32767.5f;
      break;
    }
    default: {
      return false;
    }
  }
  /* Try setting the requested range */
  if (!WriteRegister(GYRO_CONFIG_, requested_range)) {
    return false;
  }
  /* Update stored range and scale */
  gyro_range_ = requested_range;
  gyro_scale_ = requested_scale;
  return true;
}
bool Mpu9250::ConfigSrd(const uint8_t srd) {
  spi_clock_ = 1000000;
  /* Changing the SRD to allow us to set the magnetometer successfully */
  if (!WriteRegister(SMPLRT_DIV_, 19)) {
    return false;
  }
  /* Set the magnetometer sample rate */
  if (srd > 9) {
    /* Set AK8963 to power down */
    WriteAk8963Register(AK8963_CNTL1_, AK8963_PWR_DOWN_);
    delay(100);  // long wait between AK8963 mode changes
    /* Set AK8963 to 16 bit resolution, 8 Hz update rate */
    if (!WriteAk8963Register(AK8963_CNTL1_, AK8963_CNT_MEAS1_)) {
      return false;
    }
    delay(100);  // long wait between AK8963 mode changes
    /* Instruct the MPU9250 to get 7 bytes from the AK8963 at the sample rate */
    uint8_t mag_data[7];
    if (!ReadAk8963Registers(AK8963_HXL_, sizeof(mag_data), mag_data)) {
      return false;
    }
  } else {
    /* Set AK8963 to power down */
    WriteAk8963Register(AK8963_CNTL1_, AK8963_PWR_DOWN_);
    delay(100);  // long wait between AK8963 mode changes
    /* Set AK8963 to 16 bit resolution, 100 Hz update rate */
    if (!WriteAk8963Register(AK8963_CNTL1_, AK8963_CNT_MEAS2_)) {
      return false;
    }
    delay(100);  // long wait between AK8963 mode changes
    /* Instruct the MPU9250 to get 7 bytes from the AK8963 at the sample rate */
    uint8_t mag_data[7];
    if (!ReadAk8963Registers(AK8963_HXL_, sizeof(mag_data), mag_data)) {
      return false;
    }
  }
  /* Set the IMU sample rate */
  if (!WriteRegister(SMPLRT_DIV_, srd)) {
    return false;
  }
  srd_ = srd;
  return true;
}
bool Mpu9250::ConfigDlpf(const DlpfBandwidth dlpf) {
  DlpfBandwidth requested_dlpf;
  spi_clock_ = 1000000;
  /* Check input is valid and set requested dlpf */
  switch (dlpf) {
    case DLPF_BANDWIDTH_184HZ: {
      requested_dlpf = dlpf;
      break;
    }
    case DLPF_BANDWIDTH_92HZ: {
      requested_dlpf = dlpf;
      break;
    }
    case DLPF_BANDWIDTH_41HZ: {
      requested_dlpf = dlpf;
      break;
    }
    case DLPF_BANDWIDTH_20HZ: {
      requested_dlpf = dlpf;
      break;
    }
    case DLPF_BANDWIDTH_10HZ: {
      requested_dlpf = dlpf;
      break;
    }
    case DLPF_BANDWIDTH_5HZ: {
      requested_dlpf = dlpf;
      break;
    }
    default: {
      return false;
    }
  }
  /* Try setting the dlpf */
  if (!WriteRegister(ACCEL_CONFIG2_, requested_dlpf)) {
    return false;
  }
  if (!WriteRegister(CONFIG_, requested_dlpf)) {
    return false;
  }
  /* Update stored dlpf */
  dlpf_bandwidth_ = requested_dlpf;
  return true;
}
void Mpu9250::DrdyCallback(uint8_t int_pin, void (*function)()) {
  pinMode(int_pin, INPUT);
  attachInterrupt(int_pin, function, RISING);
}
bool Mpu9250::Read() {
  spi_clock_ = 20000000;
  /* Read the data registers */
  uint8_t data_buff[22];
  if (!ReadRegisters(INT_STATUS_, sizeof(data_buff), data_buff)) {
    return false;
  }
  /* Check if data is ready */
  bool data_ready = (data_buff[0] & RAW_DATA_RDY_INT_);
  if (!data_ready) {
    return false;
  }
  /* Unpack the buffer */
  accel_counts[0] = static_cast<int16_t>(data_buff[1])  << 8 | data_buff[2];
  accel_counts[1] = static_cast<int16_t>(data_buff[3])  << 8 | data_buff[4];
  accel_counts[2] = static_cast<int16_t>(data_buff[5])  << 8 | data_buff[6];
  temp_counts =     static_cast<int16_t>(data_buff[7])  << 8 | data_buff[8];
  gyro_counts[0] =  static_cast<int16_t>(data_buff[9])  << 8 | data_buff[10];
  gyro_counts[1] =  static_cast<int16_t>(data_buff[11]) << 8 | data_buff[12];
  gyro_counts[2] =  static_cast<int16_t>(data_buff[13]) << 8 | data_buff[14];
  mag_counts[0] =   static_cast<int16_t>(data_buff[16]) << 8 | data_buff[15];
  mag_counts[1] =   static_cast<int16_t>(data_buff[18]) << 8 | data_buff[17];
  mag_counts[2] =   static_cast<int16_t>(data_buff[20]) << 8 | data_buff[19];
  /* Convert to float values and rotate the accel / gyro axis */
  accel_mps2_[0] = static_cast<float>(accel_counts[1]) * accel_scale_ *
                   9.80665f;
  accel_mps2_[2] = static_cast<float>(accel_counts[2]) * accel_scale_ *
                   -9.80665f;
  accel_mps2_[1] = static_cast<float>(accel_counts[0]) * accel_scale_ *
                   9.80665f;
  die_temperature_c_ = (static_cast<float>(temp_counts) - 21.0f) / temp_scale_
                     + 21.0f;
  gyro_radps_[1] = static_cast<float>(gyro_counts[0]) * gyro_scale_ *
                   3.14159265358979323846f / 180.0f;
  gyro_radps_[0] = static_cast<float>(gyro_counts[1]) * gyro_scale_ *
                   3.14159265358979323846f / 180.0f;
  gyro_radps_[2] = static_cast<float>(gyro_counts[2]) * gyro_scale_ *
                   -1.0f * 3.14159265358979323846f / 180.0f;
  mag_ut_[0] =   static_cast<float>(mag_counts[0]) * mag_scale_[0];
  mag_ut_[1] =   static_cast<float>(mag_counts[1]) * mag_scale_[1];
  mag_ut_[2] =   static_cast<float>(mag_counts[2]) * mag_scale_[2];
  return true;
}
bool Mpu9250::WriteRegister(uint8_t reg, uint8_t data) {
  uint8_t ret_val;
  if (iface_ == I2C) {
    i2c_->beginTransmission(conn_);
    i2c_->write(reg);
    i2c_->write(data);
    i2c_->endTransmission();
  } else {
    spi_->beginTransaction(SPISettings(spi_clock_, MSBFIRST, SPI_MODE3));
    #if defined(__MK20DX128__) || defined(__MK20DX256__) || \
        defined(__MK64FX512__) || defined(__MK66FX1M0__) || \
        defined(__MKL26Z64__)  || defined(__IMXRT1062__) || \
        defined(__IMXRT1052__)
    digitalWriteFast(conn_, LOW);
    #else
    digitalWrite(conn_, LOW);
    #endif
    #if defined(__IMXRT1062__)
      delayNanoseconds(200);
    #endif
    spi_->transfer(reg);
    spi_->transfer(data);
    #if defined(__MK20DX128__) || defined(__MK20DX256__) || \
        defined(__MK64FX512__) || defined(__MK66FX1M0__) || \
        defined(__MKL26Z64__)  || defined(__IMXRT1062__) || \
        defined(__IMXRT1052__)
    digitalWriteFast(conn_, HIGH);
    #else
    digitalWrite(conn_, HIGH);
    #endif
    #if defined(__IMXRT1062__)
      delayNanoseconds(200);
    #endif
    spi_->endTransaction();
  }
  delay(10);
  ReadRegisters(reg, sizeof(ret_val), &ret_val);
  if (data == ret_val) {
    return true;
  } else {
    return false;
  }
}
bool Mpu9250::ReadRegisters(uint8_t reg, uint8_t count, uint8_t *data) {
  if (iface_ == I2C) {
    i2c_->beginTransmission(conn_);
    i2c_->write(reg);
    i2c_->endTransmission(false);
    uint8_t bytes_rx = i2c_->requestFrom(conn_, count);
    if (bytes_rx == count) {
      for (int i = 0; i < count; i++) {
        data[i] = i2c_->read();
      }
      return true;
    } else {
      return false;
    }
  } else {
    spi_->beginTransaction(SPISettings(spi_clock_, MSBFIRST, SPI_MODE3));
    #if defined(__MK20DX128__) || defined(__MK20DX256__) || \
        defined(__MK64FX512__) || defined(__MK66FX1M0__) || \
        defined(__MKL26Z64__)  || defined(__IMXRT1062__) || \
        defined(__IMXRT1052__)
    digitalWriteFast(conn_, LOW);
    #else
    digitalWrite(conn_, LOW);
    #endif
    #if defined(__IMXRT1062__)
      delayNanoseconds(200);
    #endif
    spi_->transfer(reg | SPI_READ_);
    spi_->transfer(data, count);
    #if defined(__MK20DX128__) || defined(__MK20DX256__) || \
        defined(__MK64FX512__) || defined(__MK66FX1M0__) || \
        defined(__MKL26Z64__)  || defined(__IMXRT1062__) || \
        defined(__IMXRT1052__)
    digitalWriteFast(conn_, HIGH);
    #else
    digitalWrite(conn_, LOW);
    #endif
    #if defined(__IMXRT1062__)
      delayNanoseconds(200);
    #endif
    spi_->endTransaction();
    return true;
  }
}
bool Mpu9250::WriteAk8963Register(uint8_t reg, uint8_t data) {
  uint8_t ret_val;
  if (!WriteRegister(I2C_SLV0_ADDR_, AK8963_I2C_ADDR_)) {
    return false;
  }
  if (!WriteRegister(I2C_SLV0_REG_, reg)) {
    return false;
  }
  if (!WriteRegister(I2C_SLV0_DO_, data)) {
    return false;
  }
  if (!WriteRegister(I2C_SLV0_CTRL_, I2C_SLV0_EN_ | sizeof(data))) {
    return false;
  }
  if (!ReadAk8963Registers(reg, sizeof(ret_val), &ret_val)) {
    return false;
  }
  if (data == ret_val) {
    return true;
  } else {
    return false;
  }
}
bool Mpu9250::ReadAk8963Registers(uint8_t reg, uint8_t count, uint8_t *data) {
  if (!WriteRegister(I2C_SLV0_ADDR_, AK8963_I2C_ADDR_ | I2C_READ_FLAG_)) {
    return false;
  }
  if (!WriteRegister(I2C_SLV0_REG_, reg)) {
    return false;
  }
  if (!WriteRegister(I2C_SLV0_CTRL_, I2C_SLV0_EN_ | count)) {
    return false;
  }
  delay(1);
  return ReadRegisters(EXT_SENS_DATA_00_, count, data);
}
