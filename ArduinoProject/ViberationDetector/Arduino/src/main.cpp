#include <Arduino.h>
#include "mpu9250.h"
#include "arduinoFFT.h"

#define SAMPLES 1024             //Must be a power of 2
#define SAMPLING_FREQUENCY 900 //Hz, must be less than 10000 due to ADC
 
arduinoFFT FFT = arduinoFFT();
 
unsigned int sampling_period_us;
unsigned long microseconds;
 
double vReal[SAMPLES];
double vImag[SAMPLES];

Mpu9250 mpu9250(&Wire, 0x68);



void setup() {

  // speed up the IIC clock rate to ensure capture the right data at the right time
  Wire.setClock(400000);
  Serial.begin(115200);

  // initianlize the MPU9250
  if(!mpu9250.Begin()){
    Serial.println("MPU9250 INIT FAILED.");
    // if init failed, then block the program
    while(1){}
  }

  // set the lowpass filter threshold to 5hz
  mpu9250.ConfigDlpf(Mpu9250::DLPF_BANDWIDTH_5HZ);
  mpu9250.ConfigAccelRange(Mpu9250::ACCEL_RANGE_2G);

  // set the sampling period
  sampling_period_us = round(1000000*(1.0/SAMPLING_FREQUENCY));
}

void loop() {
  /*SAMPLING*/
    for(int i=0; i<SAMPLES; i++)
    {
        microseconds = micros();    //Overflows after around 70 minutes!

        mpu9250.Read();
        vReal[i] = mpu9250.accel_counts[2];
        Serial.println(vReal[i]);
        vImag[i] = 0;
     
        while(micros() < (microseconds + sampling_period_us)){
        }
    }

    /*FFT*/
    FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD);
    FFT.ComplexToMagnitude(vReal, vImag, SAMPLES);
    double peak = FFT.MajorPeak(vReal, SAMPLES, SAMPLING_FREQUENCY);
 
    /*PRINT RESULTS*/
    //Serial.println(peak);     //Print out what frequency is the most dominant.


    Serial.println("BOF");
    for(int i=0; i<(SAMPLES/2); i++)
    {
        /*View all these three lines in serial terminal to see which frequencies has which amplitudes*/
        Serial.print((i * 1.0 * SAMPLING_FREQUENCY) / SAMPLES, 1);
        Serial.print(",");
        Serial.println(vReal[i], 1);    //View only this line in serial plotter to visualize the bins
    }

    Serial.println("EOF");


}