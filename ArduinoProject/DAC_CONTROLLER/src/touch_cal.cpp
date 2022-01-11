// from TFT_eSPI/examples/Generic/Touch_calibrate/Touch_calibrate.ino

#include "touch_cal.hpp"

#if TOUCH_CAL
extern TFT_eSPI tft;

void touch_init(){
    // Initialise the TFT screen
    tft.begin();

    // Set the rotation
    tft.setRotation(1);

    // Calibrate the touch screen and retrieve the scaling factors
    // touch_calibrate();

    uint16_t calData[5] = { 370, 3586, 196, 3579, 7 };
    tft.setTouch(calData);

    // fill the screen
    tft.fillScreen(TFT_BLACK);
}

void touch_calibrate()
{
    uint16_t calData[5];
    uint8_t calDataOK = 0;

    // Calibrate
    tft.fillScreen(TFT_BLACK);
    tft.setCursor(20, 0);
    tft.setTextFont(2);
    tft.setTextSize(1);
    tft.setTextColor(TFT_WHITE, TFT_BLACK);

    tft.println("Touch corners as indicated");

    tft.setTextFont(1);
    tft.println();

    tft.calibrateTouch(calData, TFT_MAGENTA, TFT_BLACK, 15);

    Serial.println(); Serial.println();
    Serial.println("// Use this calibration code in setup():");
    Serial.print("  uint16_t calData[5] = ");
    Serial.print("{ ");

    for (uint8_t i = 0; i < 5; i++)
    {
        Serial.print(calData[i]);
        if (i < 4) Serial.print(", ");
    }

    Serial.println(" };");
    Serial.print("  tft.setTouch(calData);");
    Serial.println(); Serial.println();

    tft.fillScreen(TFT_BLACK);
    
    tft.setTextColor(TFT_GREEN, TFT_BLACK);
    tft.println("Calibration complete!");
    tft.println("Calibration code sent to Serial port.");

    delay(4000);
}

#endif