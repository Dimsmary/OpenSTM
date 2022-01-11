#include "lvgl_control.hpp"

extern TFT_eSPI tft;

/* Render Buffer */
static lv_disp_buf_t disp_buf;
static lv_color_t buf[LV_HOR_RES_MAX * 10];

/* Multi Task */
void multitask_lgvl(void * parameters){
  for(;;){
    lv_task_handler(); /* let the GUI do its work */
    vTaskDelay(5 / portTICK_PERIOD_MS);
  }
}

/* Display flushing */
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p)
{
    uint32_t w = (area->x2 - area->x1 + 1);
    uint32_t h = (area->y2 - area->y1 + 1);

    tft.startWrite();
    tft.setAddrWindow(area->x1, area->y1, w, h);
    tft.pushColors(&color_p->full, w * h, true);
    tft.endWrite();

    lv_disp_flush_ready(disp);
}

/*Read the touchpad*/
bool my_touchpad_read(lv_indev_drv_t * indev_driver, lv_indev_data_t * data)
{
    uint16_t touchX, touchY;

    bool touched = tft.getTouch(&touchX, &touchY, 600);

    if(!touched) {
      data->state = LV_INDEV_STATE_REL;
    } else {
      data->state = LV_INDEV_STATE_PR;
	
      /*Set the coordinates*/
      data->point.x = touchX;
      data->point.y = touchY;

      Serial.print("Data x");
      Serial.println(touchX);

      Serial.print("Data y");
      Serial.println(touchY);
    }

    return false; /*Return `false` because we are not buffering and no more data to read*/
}

void lvgl_control_init(){

  lv_init();
  tft.begin(); /* TFT init */
  tft.setRotation(1); /* Landscape orientation */
  uint16_t calData[5] = {370, 3586, 196, 3579, 7 };
  tft.setTouch(calData);
  lv_disp_buf_init(&disp_buf, buf, NULL, LV_HOR_RES_MAX * 10);
  /*Initialize the display*/
  lv_disp_drv_t disp_drv;
  lv_disp_drv_init(&disp_drv);
  disp_drv.hor_res = 320;
  disp_drv.ver_res = 240;
  disp_drv.flush_cb = my_disp_flush;
  disp_drv.buffer = &disp_buf;
  lv_disp_drv_register(&disp_drv);

  /*Initialize the (dummy) input device driver*/
  lv_indev_drv_t indev_drv;
  lv_indev_drv_init(&indev_drv);
  indev_drv.type = LV_INDEV_TYPE_POINTER;
  indev_drv.read_cb = my_touchpad_read;
  lv_indev_drv_register(&indev_drv);

  /* Create GUI Widgets */
  GUI_init();
  // lv_demo_widgets();

  /* Create a task for lvgl */
  xTaskCreate(
    multitask_lgvl, // task function
    "lvgl_task", // task name
    20000, // stack size
    NULL, // task parameters
    1, // priority
    NULL // task handle
    );
}