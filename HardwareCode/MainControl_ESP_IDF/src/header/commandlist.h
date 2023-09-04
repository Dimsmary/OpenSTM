#ifndef COMMANDLIST_H
#define COMMANDLIST_H

#define SYSTEM_COMMAND_SET_16b  "SETD0"
#define SYSTEM_COMMAND_SET_DZ   "SETD1"
#define SYSTEM_COMMAND_SET_DX   "SETD2"
#define SYSTEM_COMMAND_SET_DY   "SETD3"
#define SYSTEM_COMMAND_SET_12b  "SETD4"
#define SYSTEM_VERSION          "VERSI"
#define SYSTEM_GET_ADC          "GETAD"
#define CURVE_STATUS            "CURVE"
#define RUN_TIME                "RUNTI"

// --> Approach
#define APPROACH_BEGIN          "APPGO"
#define APPROACH_STOP           "APPST"
#define APPROACH_OK             "APPOK"
#define APPROACH_REGISTER       "APPRE"
#define APPROACH_TARGET         "APPTA"
#define APPROACH_SLIDER_STEP    "APPSS"
#define APPROACH_SET_KP         "APPS0"
#define APPROACH_SET_KI         "APPS1"
#define APPROACH_SET_KD         "APPS2"
#define APPROACH_CRASH          "APPCA"
#define APPROACH_S_AMPLITUDE    "APPAM"
#define APPROACH_S_SLOPE        "APPSO"
#define APPROACH_S_SLOW         "APPSL"
#define APPROACH_S_FAST         "APPFA"
#define APPROACH_BIAS           "APPBI"

#define APPROACH_RETURN_PUNCH   "APPPU"
#define APPROACH_RETURN_STATUS  "APPST"
#define APPROACH_RETURN_PID     "APPPI"

// --> Curve Test
#define CURVE_TEST_REG          "CTREG"
#define CURVE_TEST_DI_STOP      "CTDST"
#define CURVE_TEST_DI_INCREMENT "CTDIN"
#define CURVE_TEST_DI_FINISHED  "CTDFI"
#define CURVE_TEST_DI_ZPOS      "CTDZP"
#define CURVE_TEST_DI_CURRENT   "CTDCU"
#define CURVE_TEST_DI_OK        "CTDOK"

#define CURVE_TEST_BI_STOP      "CTBST"
#define CURVE_TEST_BI_INCREMENT "CTBIN"
#define CURVE_TEST_BI_START     "CTBSS"
#define CURVE_TEST_BI_FINISHED  "CTBFI"
#define CURVE_TEST_BI_CURRENT   "CTBCU"
#define CURVE_TEST_BI_BIAS      "CTBBI"
#define CURVE_TEST_BI_OK        "CTBOK"

#define CURVE_TEST_DELAY        "CTDLY"

#define CURVE_TEST_RESET        "CTRST"

// --> Scan
#define SCAN_REG                "SCREG"

#define SCAN_LINE_TARGET        "SCLTA"
#define SCAN_LINE_ORIGIN_X      "SCLTX"
#define SCAN_LINE_ORIGIN_Y      "SCLTY"
#define SCAN_LINE_INC           "SCLIN"
#define SCAN_LINE_DIRECTION     "SCLDI"
#define SCAN_CCCH_MODE          "SCCMO"

#define SCAN_LINE_POSITION      "SCLP0"
#define SCAN_LINE_CURRENT       "SCLC0"

#define SCAN_LINE_POSITION_1    "SCLP1"
#define SCAN_LINE_CURRENT_1     "SCLC1"

#define SCAN_LINE_OK            "SCLOK"

#define SCAN_X_BEGIN            "SCXBE"
#define SCAN_X_END              "SCXEN"
#define SCAN_Y_BEGIN            "SCYBE"
#define SCAN_Y_END              "SCYEN"
#define SCAN_INC                "SCINC"
#define SCAN_CC_INC             "SCCIN"
#define SCAN_MODE               "SCMOD"
#define SCAN_POS_X              "SCPOX"
#define SCAN_POS_Y              "SCPOY"
#define SCAN_CURRENT            "SCCUR"
#define SCAN_OK                 "SCOKO"
#define SCAN_RETRACT            "SCRET"
#define SCAN_EZ                 "SCEZS"

#define SCAN_DELAY              "SCDLY"

#endif