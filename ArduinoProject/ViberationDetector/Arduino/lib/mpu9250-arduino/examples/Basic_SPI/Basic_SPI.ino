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

#include "mpu9250.h"

/* An Mpu9250 object on SPI bus 0 with chip select 10 */
Mpu9250 imu(&SPI, 10);
int status;

void setup() {
  /* Serial to display data */
  Serial.begin(115200);
  while(!Serial) {}
  /* Start communication */
  if (!imu.Begin()) {
    Serial.println("IMU initialization unsuccessful");
    while(1) {}
  }
}

void loop() {
  /* Read the sensor */
  if (imu.Read()) {
    /* Display the data */
    Serial.print(imu.accel_x_mps2(), 6);
    Serial.print("\t");
    Serial.print(imu.accel_y_mps2(), 6);
    Serial.print("\t");
    Serial.print(imu.accel_z_mps2(), 6);
    Serial.print("\t");
    Serial.print(imu.gyro_x_radps(), 6);
    Serial.print("\t");
    Serial.print(imu.gyro_y_radps(), 6);
    Serial.print("\t");
    Serial.print(imu.gyro_z_radps(), 6);
    Serial.print("\t");
    Serial.print(imu.mag_x_ut(), 6);
    Serial.print("\t");
    Serial.print(imu.mag_y_ut(), 6);
    Serial.print("\t");
    Serial.print(imu.mag_z_ut(), 6);
    Serial.print("\t");
    Serial.println(imu.die_temperature_c(), 6);
  }
  delay(100);
}
