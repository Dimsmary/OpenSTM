#include "lvgl_control_approach.hpp"

/* Static Variables */
static lv_obj_t * tabview;
static lv_obj_t * tab_approach;
static lv_obj_t * tab_scan;
static lv_obj_t * tab_result;

// Tab Approach
static lv_obj_t * approach_slider;
static lv_obj_t * approach_label_sliderVoltage;
static lv_obj_t * approach_label_sliderRegister;
static lv_obj_t * approach_checkbox_1MX;
static lv_obj_t * approach_checkbox_1KX;
static lv_obj_t * approach_checkbox_100X;
static lv_obj_t * approach_checkbox_10X;
static lv_obj_t * approach_checkbox_1X;
static lv_obj_t * approach_btn_add;
static lv_obj_t * approach_btn_minus;
static lv_obj_t * approach_register_now;
static lv_obj_t * approach_voltage_now;
static lv_obj_t * approach_adc_register;
static lv_obj_t * approach_adc_voltage;
static lv_obj_t * approach_btn_follow;
static lv_obj_t * approach_btn_power;
static lv_obj_t * approach_btn_tip_follow;
static lv_obj_t * approach_btn_tip_power;
static lv_obj_t * approach_btn_follow_adc;
static lv_obj_t * approach_btn_scan;
static lv_obj_t * approach_slider_scan_period;
static lv_obj_t * approach_slider_scan_step;
static lv_obj_t * approach_label_scan_period;
static lv_obj_t * approach_label_scan_step;
static lv_obj_t * approach_label_tip_voltage;
static lv_obj_t * approach_label_tip_register;
static lv_obj_t * approach_adc_read_voltage;
static lv_obj_t * approach_adc_read_register;

/* DAC and ADC Value */
int Z_register_buff = 0x7fff;


/* Public */
int tip_register = 0x7fff;
int Z_register_update= 0x7fff;
bool is_z_power = false;
bool is_tip_power = false;
int ADC_register_th = 0;
int scan_period = 1;
int scan_step = 15;
bool scan_direction = SCAN_FORWARD;

/* GUI Variables*/

// checkbox scal 0 stand for checked 1X
uint8_t check_box_scale = 0;

/**********************/
/*** RETURNING HERE***/
/********************/

// z_register -- Z axis piezo crystal DAC voltage (DAC#0)
// tip_register -- The voltage between sample and tip (DAC#1)

int approach_get_z_power(){
    return is_z_power;
}

int approach_get_tip_power(){
    return is_tip_power;
}

int approach_get_z_register(){
    return Z_register_update;
}

int approach_get_tip_register(){
    return tip_register;
}


/*********************************/
/*** CALCULATION FUNCTONS HERE***/
/*******************************/
// return the mapping from dac/adc register to voltage
String dac_register_to_voltage(int register_val){
    return String(register_val * (20.00 / 65535) - 10); 
}

String adc_register_to_voltage(int register_val){
    return String(register_val * (4.096 / 65535)); 
}

void adc_register_update(int register_val, lv_obj_t * label_register, lv_obj_t * label_voltage){
    String text_val = "#4bc230 " + String(register_val) + "#";
    // turn Arduino String into char array
    char buf[20];
    text_val.toCharArray(buf, 20);
    // update the label value
    lv_label_set_text(label_register, buf);
    // mapping the voltage from register value
    String voltage = "#4bc230 " + adc_register_to_voltage(register_val) + "V#";
    voltage.toCharArray(buf, 20);
    lv_label_set_text(label_voltage, buf);
}

void dac_register_update(int register_val, lv_obj_t * label_register, lv_obj_t * label_voltage){
    String text_val = "#005780 " + String(register_val) + "#";
    // turn Arduino String into char array
    char buf[20];
    text_val.toCharArray(buf, 20);
    // update the label value
    lv_label_set_text(label_register, buf);
    // mapping the voltage from register value
    String voltage = "#800000 " + dac_register_to_voltage(register_val) + "V#";
    voltage.toCharArray(buf, 20);
    lv_label_set_text(label_voltage, buf);
}

void DAC_ADC_display_update(){
    // update the value of slider display label
    dac_register_update(Z_register_buff, approach_label_sliderRegister, approach_label_sliderVoltage);
    // if DAC-FOLLOW button is on, then sync the value from register_buff to register_update
    if(lv_btn_get_state(approach_btn_follow) == LV_BTN_STATE_CHECKED_RELEASED){
        Z_register_update = Z_register_buff;
        dac_register_update(Z_register_update, approach_register_now, approach_voltage_now);

    }

    // if ADC-FOLLOW is on
    if(lv_btn_get_state(approach_btn_follow_adc) == LV_BTN_STATE_CHECKED_RELEASED){
        ADC_register_th = Z_register_buff;
        adc_register_update(ADC_register_th, approach_adc_register, approach_adc_voltage);
    }

    // if TIP-FOLLOW is on
    if(lv_btn_get_state(approach_btn_tip_follow) == LV_BTN_STATE_CHECKED_RELEASED){
        tip_register = Z_register_buff;
        dac_register_update(tip_register, approach_label_tip_register, approach_label_tip_voltage);
    }

}

/*******************************/
/*** CALL BACK FUNCTONS HERE***/
/*****************************/
// Approach Tab
// Z axis slider
void approach_slider_cb(lv_obj_t * slider, lv_event_t event){

    // If slider value has changed
    if(event == LV_EVENT_VALUE_CHANGED){
        // get the value from slider
        // map slider value to 16bit register value
        Z_register_buff = lv_slider_get_value(approach_slider) * 15;
        // update the display value
        DAC_ADC_display_update();
    }
}

// button
void approach_btn_add_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_CLICKED){
        // calculate the new register value
        int new_z_register = Z_register_buff + pow(10, check_box_scale);
        // if new value is not overflow, then update the slider
        if(new_z_register < 65536){
            Z_register_buff = new_z_register;   
        }
        else{
            Z_register_buff = 65535;
        }
        lv_slider_set_value(approach_slider, new_z_register / 15, LV_ANIM_ON);
        DAC_ADC_display_update();
    }
}

void approach_btn_minus_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_CLICKED){
        // calculate the new register value
        int new_z_register = Z_register_buff - pow(10, check_box_scale);
        // if new value is not overflow, then update the slider
        if(new_z_register > -1){
            Z_register_buff = new_z_register;
        }
        else{
            Z_register_buff = 0;
        }
        lv_slider_set_value(approach_slider, new_z_register / 15, LV_ANIM_ON);
        DAC_ADC_display_update();
    }
}

void approach_btn_follow_cb(lv_obj_t * obj, lv_event_t event){
    // Sync the value from dac buffer to slider buffer
    lv_slider_set_value(approach_slider, Z_register_update / 15, LV_ANIM_ON);
    Z_register_buff = Z_register_update;
    DAC_ADC_display_update();
}

void approach_btn_tip_follow_cb(lv_obj_t * obj, lv_event_t event){
    // Sync the value from dac buffer to slider buffer
    lv_slider_set_value(approach_slider, tip_register / 15, LV_ANIM_ON);
    Z_register_buff = tip_register;
    DAC_ADC_display_update();
}

void approach_btn_follow_adc_cb(lv_obj_t * obj, lv_event_t event){
    // Sync the value from adc buffer to slider buffer
    lv_slider_set_value(approach_slider, ADC_register_th / 15, LV_ANIM_ON);
    Z_register_buff = ADC_register_th;
    DAC_ADC_display_update();
}

void approach_btn_power_cb(lv_obj_t * obj, lv_event_t event){
    // Change the power status
    if(lv_btn_get_state(approach_btn_power) == LV_BTN_STATE_CHECKED_RELEASED){
        is_z_power = true;
    }else{
        is_z_power = false;
    }
}

void approach_btn_tip_power_cb(lv_obj_t * obj, lv_event_t event){
    // Change the power status
    if(lv_btn_get_state(approach_btn_tip_power) == LV_BTN_STATE_CHECKED_RELEASED){
        is_tip_power = true;
    }else{
        is_tip_power = false;
    }
}


// Other slider
void approach_slider_scan_period_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_VALUE_CHANGED){
        // get the value from slider
        static char buf[20];
        String value = String(lv_slider_get_value(approach_slider_scan_period));
        value = "Peroid = " + value + "Hz";
        value.toCharArray(buf, 20);
        // update the display value
        lv_label_set_text(approach_label_scan_period, buf);
    }
}

void approach_slider_scan_step_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_VALUE_CHANGED){
        // get the value from slider
        static char buf[20];
        String value = String(lv_slider_get_value(approach_slider_scan_step));
        value = "Step = " + value;
        value.toCharArray(buf, 20);
        // update the display value
        lv_label_set_text(approach_label_scan_step, buf);
    }
}


// check boxs
void uncheck_all(){
    // uncheck all the checkboxs and set the flag
    lv_checkbox_set_checked(approach_checkbox_1MX, false);
    lv_checkbox_set_checked(approach_checkbox_1KX, false);
    lv_checkbox_set_checked(approach_checkbox_100X, false);
    lv_checkbox_set_checked(approach_checkbox_10X, false);
    lv_checkbox_set_checked(approach_checkbox_1X, false);
}

void approach_checkbox_1MX_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_VALUE_CHANGED){
        uncheck_all();
        lv_checkbox_set_checked(approach_checkbox_1MX, true);
        check_box_scale = 4;
    }
}

void approach_checkbox_1KX_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_VALUE_CHANGED){
        uncheck_all();
        lv_checkbox_set_checked(approach_checkbox_1KX, true);
        check_box_scale = 3;
    }
}

void approach_checkbox_100X_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_VALUE_CHANGED){
        uncheck_all();
        lv_checkbox_set_checked(approach_checkbox_100X, true);
        check_box_scale = 2;
    }
}

void approach_checkbox_10X_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_VALUE_CHANGED){
        uncheck_all();
        lv_checkbox_set_checked(approach_checkbox_10X, true);
        check_box_scale = 1;
    }
}

void approach_checkbox_1X_cb(lv_obj_t * obj, lv_event_t event){
    if(event == LV_EVENT_VALUE_CHANGED){
        uncheck_all();
        lv_checkbox_set_checked(approach_checkbox_1X, true);
        check_box_scale = 0;
    }
}


/*********************/
/*** GUI INIT HERE***/
/*******************/
void GUI_init(){
    /** Tab View **/
    tabview = lv_tabview_create(lv_scr_act(), NULL);
    tab_approach = lv_tabview_add_tab(tabview, "Approach");
    tab_scan = lv_tabview_add_tab(tabview, "Scan");
    tab_result = lv_tabview_add_tab(tabview, "Result");

    /* Tab Approach Wedgets */
    approach_label_sliderRegister = lv_label_create(tab_approach, NULL);
    approach_label_sliderVoltage = lv_label_create(tab_approach, NULL);
    
    // labels
    lv_label_set_align(approach_label_sliderRegister, LV_LABEL_ALIGN_LEFT);
    lv_label_set_align(approach_label_sliderVoltage, LV_LABEL_ALIGN_LEFT);

    lv_label_set_recolor(approach_label_sliderRegister, true);
    lv_label_set_recolor(approach_label_sliderVoltage, true);

    lv_label_set_text(approach_label_sliderRegister, "#005780 32767#");
    lv_label_set_text(approach_label_sliderVoltage, "#800000 0.00V#");
    
    lv_obj_align(approach_label_sliderRegister, NULL, LV_ALIGN_IN_TOP_LEFT, 10, 15);
    lv_obj_align(approach_label_sliderVoltage, approach_label_sliderRegister, LV_ALIGN_OUT_RIGHT_MID, 5, 0);

    approach_adc_read_register = lv_label_create(tab_approach, NULL);
    approach_adc_read_voltage = lv_label_create(tab_approach, NULL);

    lv_label_set_align(approach_adc_read_register, LV_LABEL_ALIGN_LEFT);
    lv_label_set_align(approach_adc_read_voltage, LV_LABEL_ALIGN_LEFT);

    lv_label_set_recolor(approach_adc_read_register, true);
    lv_label_set_recolor(approach_adc_read_voltage, true);

    lv_label_set_text(approach_adc_read_register, "#4bc230 00000#");
    lv_label_set_text(approach_adc_read_voltage, "#4bc230 0.00V#");
    
    lv_obj_align(approach_adc_read_register, approach_label_sliderVoltage, LV_ALIGN_OUT_RIGHT_MID, 10, 0);
    lv_obj_align(approach_adc_read_voltage, approach_adc_read_register, LV_ALIGN_OUT_RIGHT_MID, 5, 0);


    // buttons
    approach_btn_add = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_add, NULL, LV_ALIGN_IN_TOP_RIGHT, 65, 8);
    lv_obj_t * label;
    label = lv_label_create(approach_btn_add, NULL);
    lv_label_set_text(label, "+");
    lv_obj_set_width(approach_btn_add, 45);
    lv_obj_set_height(approach_btn_add, 30);
    lv_obj_set_event_cb(approach_btn_add, approach_btn_add_cb);

    approach_btn_minus = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_minus, NULL, LV_ALIGN_IN_TOP_RIGHT, 15, 8);
    label = lv_label_create(approach_btn_minus, NULL);
    lv_label_set_text(label, "-");
    lv_obj_set_width(approach_btn_minus, 45);
    lv_obj_set_height(approach_btn_minus, 30);
    lv_obj_set_event_cb(approach_btn_minus, approach_btn_minus_cb);

    // slider
    approach_slider = lv_slider_create(tab_approach, NULL);
    lv_obj_align(approach_slider, NULL, LV_ALIGN_CENTER, 0, -40);
    lv_obj_set_event_cb(approach_slider, approach_slider_cb);
    lv_slider_set_range(approach_slider, 0, 4369);
    lv_slider_set_value(approach_slider, Z_register_buff / 15, LV_ANIM_ON);

    // Checkbox
    approach_checkbox_1MX = lv_checkbox_create(tab_approach, NULL);
    lv_checkbox_set_text(approach_checkbox_1MX, "1MX");
    lv_obj_align(approach_checkbox_1MX, approach_slider, LV_ALIGN_OUT_BOTTOM_LEFT, -20 , 15);
    lv_obj_set_event_cb(approach_checkbox_1MX, approach_checkbox_1MX_cb);

    approach_checkbox_1KX = lv_checkbox_create(tab_approach, NULL);
    lv_checkbox_set_text(approach_checkbox_1KX, "1KX");
    lv_obj_align(approach_checkbox_1KX, approach_checkbox_1MX, LV_ALIGN_OUT_RIGHT_MID, 9 , 0);
    lv_obj_set_event_cb(approach_checkbox_1KX, approach_checkbox_1KX_cb);

    approach_checkbox_100X = lv_checkbox_create(tab_approach, NULL);
    lv_checkbox_set_text(approach_checkbox_100X, "100X");
    lv_obj_align(approach_checkbox_100X, approach_checkbox_1KX, LV_ALIGN_OUT_RIGHT_MID, 9 , 0);
    lv_obj_set_event_cb(approach_checkbox_100X, approach_checkbox_100X_cb);

    approach_checkbox_10X = lv_checkbox_create(tab_approach, NULL);
    lv_checkbox_set_text(approach_checkbox_10X, "10X");
    lv_obj_align(approach_checkbox_10X, approach_checkbox_100X, LV_ALIGN_OUT_RIGHT_MID, 9 , 0);
    lv_obj_set_event_cb(approach_checkbox_10X, approach_checkbox_10X_cb);

    approach_checkbox_1X = lv_checkbox_create(tab_approach, NULL);
    lv_checkbox_set_text(approach_checkbox_1X, "1X");
    lv_obj_align(approach_checkbox_1X, approach_checkbox_10X, LV_ALIGN_OUT_RIGHT_MID, 9 , 0);
    lv_obj_set_event_cb(approach_checkbox_1X, approach_checkbox_1X_cb);

    lv_checkbox_set_checked(approach_checkbox_1X, true);

    // labels new
    approach_register_now = lv_label_create(tab_approach, NULL);
    approach_voltage_now = lv_label_create(tab_approach, NULL);

    lv_label_set_align(approach_register_now, LV_LABEL_ALIGN_LEFT);
    lv_label_set_align(approach_voltage_now, LV_LABEL_ALIGN_LEFT);

    lv_label_set_recolor(approach_register_now, true);
    lv_label_set_recolor(approach_voltage_now, true);

    lv_label_set_text(approach_register_now, "#005780 32767#");
    lv_label_set_text(approach_voltage_now, "#800000 0.00V#");
    
    lv_obj_align(approach_register_now, approach_checkbox_1MX, LV_ALIGN_OUT_BOTTOM_LEFT, 4, 15);
    lv_obj_align(approach_voltage_now, approach_register_now, LV_ALIGN_OUT_RIGHT_MID, 10, 0);


    approach_label_tip_register = lv_label_create(tab_approach, NULL);
    approach_label_tip_voltage = lv_label_create(tab_approach, NULL);

    lv_label_set_align(approach_label_tip_register, LV_LABEL_ALIGN_LEFT);
    lv_label_set_align(approach_label_tip_voltage, LV_LABEL_ALIGN_LEFT);

    lv_label_set_recolor(approach_label_tip_register, true);
    lv_label_set_recolor(approach_label_tip_voltage, true);

    lv_label_set_text(approach_label_tip_register, "#005780 32767#");
    lv_label_set_text(approach_label_tip_voltage, "#800000 0.00V#");
    
    lv_obj_align(approach_label_tip_register, approach_register_now, LV_ALIGN_OUT_BOTTOM_LEFT, 0, 25);
    lv_obj_align(approach_label_tip_voltage, approach_label_tip_register, LV_ALIGN_OUT_RIGHT_MID, 10, 0);

    approach_adc_register = lv_label_create(tab_approach, NULL);
    approach_adc_voltage = lv_label_create(tab_approach, NULL);

    lv_label_set_align(approach_adc_register, LV_LABEL_ALIGN_LEFT);
    lv_label_set_align(approach_adc_voltage, LV_LABEL_ALIGN_LEFT);

    lv_label_set_recolor(approach_adc_register, true);
    lv_label_set_recolor(approach_adc_voltage, true);

    lv_label_set_text(approach_adc_register, "#4bc230 00000#");
    lv_label_set_text(approach_adc_voltage, "#4bc230 0.00V#");
    
    lv_obj_align(approach_adc_register, approach_label_tip_register, LV_ALIGN_OUT_BOTTOM_LEFT, 0, 25);
    lv_obj_align(approach_adc_voltage, approach_adc_register, LV_ALIGN_OUT_RIGHT_MID, 10, 0);

    

    // buttons
    approach_btn_follow = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_follow, NULL, LV_ALIGN_IN_TOP_RIGHT, -60, 100);
    label = lv_label_create(approach_btn_follow, NULL);
    lv_label_set_text(label, "DAC-FO");
    lv_btn_set_checkable(approach_btn_follow, true);
    lv_obj_set_width(approach_btn_follow, 80);
    lv_obj_set_height(approach_btn_follow, 30);
    lv_obj_set_event_cb(approach_btn_follow, approach_btn_follow_cb);

    approach_btn_power = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_power, NULL, LV_ALIGN_IN_TOP_RIGHT, 30, 100);
    label = lv_label_create(approach_btn_power, NULL);
    lv_label_set_text(label, "POWER");
    lv_btn_set_checkable(approach_btn_power, true);
    lv_obj_set_width(approach_btn_power, 80);
    lv_obj_set_height(approach_btn_power, 30);
    lv_obj_set_event_cb(approach_btn_power, approach_btn_power_cb);


    approach_btn_tip_follow = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_tip_follow, NULL, LV_ALIGN_IN_TOP_RIGHT, -60, 140);
    label = lv_label_create(approach_btn_tip_follow, NULL);
    lv_label_set_text(label, "TIP-FO");
    lv_btn_set_checkable(approach_btn_tip_follow, true);
    lv_obj_set_width(approach_btn_tip_follow, 80);
    lv_obj_set_height(approach_btn_tip_follow, 30);
    lv_obj_set_event_cb(approach_btn_tip_follow, approach_btn_tip_follow_cb);

    approach_btn_tip_power = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_tip_power, NULL, LV_ALIGN_IN_TOP_RIGHT, 30, 140);
    label = lv_label_create(approach_btn_tip_power, NULL);
    lv_label_set_text(label, "POWER");
    lv_btn_set_checkable(approach_btn_tip_power, true);
    lv_obj_set_width(approach_btn_tip_power, 80);
    lv_obj_set_height(approach_btn_tip_power, 30);
    lv_obj_set_event_cb(approach_btn_tip_power, approach_btn_tip_power_cb);


    approach_btn_follow_adc = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_follow_adc, NULL, LV_ALIGN_IN_TOP_RIGHT, -60, 180);
    label = lv_label_create(approach_btn_follow_adc, NULL);
    lv_label_set_text(label, "ADC-FO");
    lv_btn_set_checkable(approach_btn_follow_adc, true);
    lv_obj_set_width(approach_btn_follow_adc, 80);
    lv_obj_set_height(approach_btn_follow_adc, 30);
    lv_obj_set_event_cb(approach_btn_follow_adc, approach_btn_follow_adc_cb);

    approach_btn_scan = lv_btn_create(tab_approach, NULL);
    lv_obj_align(approach_btn_scan, NULL, LV_ALIGN_IN_TOP_RIGHT, 30, 180);
    label = lv_label_create(approach_btn_scan, NULL);
    lv_label_set_text(label, "SCAN");
    lv_btn_set_checkable(approach_btn_scan, true);
    lv_obj_set_width(approach_btn_scan, 80);
    lv_obj_set_height(approach_btn_scan, 30);

    // slider
    approach_slider_scan_period = lv_slider_create(tab_approach, NULL);
    lv_obj_align(approach_slider_scan_period, NULL, LV_ALIGN_CENTER, 0, 150);
    lv_obj_set_event_cb(approach_slider_scan_period, approach_slider_cb);
    lv_slider_set_range(approach_slider_scan_period, 1, 100);
    lv_obj_set_event_cb(approach_slider_scan_period, approach_slider_scan_period_cb);

    approach_slider_scan_step = lv_slider_create(tab_approach, NULL);
    lv_obj_align(approach_slider_scan_step, NULL, LV_ALIGN_CENTER, 0, 180);
    lv_obj_set_event_cb(approach_slider_scan_step, approach_slider_cb);
    lv_slider_set_range(approach_slider_scan_step, 1, 100);
    lv_obj_set_event_cb(approach_slider_scan_step, approach_slider_scan_step_cb);

    lv_obj_set_event_cb(approach_btn_add, approach_btn_add_cb);

    // label
    approach_label_scan_period = lv_label_create(tab_approach, NULL);
    lv_label_set_align(approach_label_scan_period, LV_LABEL_ALIGN_LEFT);
    lv_label_set_text(approach_label_scan_period, "Period = 20Hz");
    lv_obj_align(approach_label_scan_period, approach_slider_scan_period, LV_ALIGN_OUT_BOTTOM_MID, 0, 15);

    approach_label_scan_step = lv_label_create(tab_approach, NULL);
    lv_label_set_align(approach_label_scan_step, LV_LABEL_ALIGN_LEFT);
    lv_label_set_text(approach_label_scan_step, "Step = 15");
    lv_obj_align(approach_label_scan_step, approach_slider_scan_step, LV_ALIGN_OUT_BOTTOM_MID, 0, 15);



}