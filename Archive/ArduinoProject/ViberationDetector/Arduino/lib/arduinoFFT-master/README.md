arduinoFFT
==========

Fast Fourier Transform for Arduino

This is a fork from https://code.google.com/p/makefurt/ which has been abandoned since 2011.

<del>This is a C++ library for Arduino for computing FFT.</del> Now it works both on Arduino and C projects.

Tested on Arduino 1.6.11

### Installation on Arduino

Use the Arduino Library Manager to install and keep it updated. Just look for arduinoFFT. Only for Arduino 1.5+

### Manual installation on Arduino

To install this library, just place this entire folder as a subfolder in your Arduino installation

When installed, this library should look like:

Arduino\libraries\arduinoFTT              			(this library's folder)
Arduino\libraries\arduinoFTT\arduinoFTT.cpp 			(the library implementation file, uses 32 bits floats vectors)
Arduino\libraries\arduinoFTT\arduinoFTT.h   			(the library header file, uses 32 bits floats vectors)
Arduino\libraries\arduinoFTT\keywords.txt 			(the syntax coloring file)
Arduino\libraries\arduinoFTT\examples     			(the examples in the "open" menu)
Arduino\libraries\arduinoFTT\readme.md   			(this file)

### Building on Arduino

After this library is installed, you just have to start the Arduino application.
You may see a few warning messages as it's built.

To use this library in a sketch, go to the Sketch | Import Library menu and
select arduinoFTT.  This will add a corresponding line to the top of your sketch:

`#include <arduinoFTT.h>`

### TODO
* Ratio table for windowing function.
* Document windowing functions advantages and disadvantages.
* Optimize usage and arguments.
* Add new windowing functions.
<del>* Spectrum table? </del>

### API

* **arduinoFFT**(void);
* **arduinoFFT**(double *vReal, double *vImag, uint16_t samples, double samplingFrequency);
Constructor
* **~arduinoFFT**(void);
Destructor
* **ComplexToMagnitude**(double *vReal, double *vImag, uint16_t samples);
* **ComplexToMagnitude**();
* **Compute**(double *vReal, double *vImag, uint16_t samples, uint8_t dir);
* **Compute**(double *vReal, double *vImag, uint16_t samples, uint8_t power, uint8_t dir);
* **Compute**(uint8_t dir);
Calcuates the Fast Fourier Transform.
* **DCRemoval**(double *vData, uint16_t samples);
* **DCRemoval**();
Removes the DC component from the sample data.
* **MajorPeak**(double *vD, uint16_t samples, double samplingFrequency);
* **MajorPeak**();
* **MajorPeakParabola**();
Looks for and returns the frequency of the biggest spike in the analyzed signal.
* **Revision**(void);
Returns the library revision.
* **Windowing**(double *vData, uint16_t samples, uint8_t windowType, uint8_t dir);
* **Windowing**(uint8_t windowType, uint8_t dir);
Performs a windowing function on the values array. The possible windowing options are:
    * FFT_WIN_TYP_RECTANGLE
    * FFT_WIN_TYP_HAMMING
    * FFT_WIN_TYP_HANN
    * FFT_WIN_TYP_TRIANGLE
    * FFT_WIN_TYP_NUTTALL
    * FFT_WIN_TYP_BLACKMAN
    * FFT_WIN_TYP_BLACKMAN_NUTTALL
    * FFT_WIN_TYP_BLACKMAN_HARRIS
    * FFT_WIN_TYP_FLT_TOP
    * FFT_WIN_TYP_WELCH
* **Exponent**(uint16_t value);
Calculates and returns the base 2 logarithm of the given value.
