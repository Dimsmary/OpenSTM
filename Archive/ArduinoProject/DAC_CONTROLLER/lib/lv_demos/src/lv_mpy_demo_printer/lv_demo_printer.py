#!/opt/bin/lv_micropython -i
import lvgl as lv
from display_driver_utils import driver,ORIENT_LANDSCAPE
from lv_colors import lv_colors
from theme import Theme, LV_DEMO_PRINTER_BLUE,LV_DEMO_PRINTER_TITLE_PAD,LV_DEMO_PRINTER_THEME_TITLE
from theme import LV_DEMO_PRINTER_THEME_ICON,LV_DEMO_PRINTER_THEME_LABEL_WHITE,LV_DEMO_PRINTER_RED,LV_DEMO_PRINTER_GREEN
from theme import LV_DEMO_PRINTER_THEME_BTN_BORDER,LV_DEMO_PRINTER_THEME_BTN_BACK
from theme import LV_DEMO_PRINTER_THEME_BTN_CIRCLE,LV_DEMO_PRINTER_THEME_BOX_BORDER
import utime as time

try:
    import logging
except:
    import ulogging as logging


class DemoPrinter(object):
    
    def __init__(self):
        self.LV_HOR_RES = lv.scr_act().get_disp().driver.hor_res
        self.LV_VER_RES = lv.scr_act().get_disp().driver.ver_res
        # Bg positions
        self.LV_DEMO_PRINTER_BG_NONE   = -self.LV_VER_RES
        self.LV_DEMO_PRINTER_BG_FULL   =  0
        self.LV_DEMO_PRINTER_BG_NORMAL = -2 * (self.LV_VER_RES // 3)
        self.LV_DEMO_PRINTER_BG_SMALL  = -5 * (self.LV_VER_RES // 6)
        
        # Animations
        self.LV_DEMO_PRINTER_ANIM_Y       = self.LV_VER_RES // 20
        self.LV_DEMO_PRINTER_ANIM_DELAY   = 40
        self.LV_DEMO_PRINTER_ANIM_TIME    = 150
        self.LV_DEMO_PRINTER_ANIM_TIME_BG = 300
        
        self.LV_DEMO_PRINTER_BG_NORMAL = (-2 * (self.LV_VER_RES // 3))

        self.log = logging.getLogger("DemoPrinter")
        self.log.setLevel(logging.ERROR)
        
        self.icon_wifi_data = None
        self.icon_wifi_dsc = None
        self.icon_tel_data = None
        self.icon_tel_dsc = None
        self.icon_eco_data = None
        self.icon_eco_dsc = None
        self.icon_pc_data = None
        self.icon_pc_dsc = None
        
        self.img_btn_bg_1_data = None
        self.img_btn_bg_1_dsc = None
        self.img_btn_bg_2_data = None
        self.img_btn_bg_2_dsc = None
        self.img_btn_bg_3_data = None
        self.img_btn_bg_3_dsc = None
        self.img_btn_bg_4_data = None
        self.img_btn_bg_4_dsc = None

        self.img_copy_data = None
        self.img_copy_dsc = None
        self.img_print_data = None
        self.img_print_dsc = None
        self.img_scan_data = None
        self.img_scan_dsc = None
        self.img_setup_data = None
        self.img_setup_dsc = None

        self.scan_img = None
        self.bg_top = None
        self.bg_bottom = None

        self.bg_color_prev = LV_DEMO_PRINTER_BLUE
        self.bg_color_act = LV_DEMO_PRINTER_BLUE
        self.bg_top = lv.obj(lv.scr_act(),None)
        self.bg_top.set_size(self.LV_HOR_RES,self.LV_VER_RES)
        
        # read all the images fromm the raw image files

        (self.icon_wifi_data,self.icon_wifi_dsc) = self.get_icon("icon_wifi_48x34",48,34)
        (self.icon_tel_data,self.icon_tel_dsc)   = self.get_icon("icon_tel_35x35",35,35)
        (self.icon_eco_data,self.icon_eco_dsc)   = self.get_icon("icon_eco_38x34",38,34)
        (self.icon_pc_data,self.icon_pc_dsc)     = self.get_icon("icon_pc_41x33",41,33)
        
        (self.icon_bright_data,self.icon_bright_dsc) = self.get_icon("icon_bright_29x29",29,29)
        (self.icon_hue_data,self.icon_hue_dsc) = self.get_icon("icon_hue_23x23",23,23)

        (self.img_btn_bg_1_data,self.img_btn_bg_1_dsc) = self.get_icon("img_btn_bg_1_174x215",174,215)
        (self.img_btn_bg_2_data,self.img_btn_bg_2_dsc) = self.get_icon("img_btn_bg_2_174x215",174,215)
        (self.img_btn_bg_3_data,self.img_btn_bg_3_dsc) = self.get_icon("img_btn_bg_3_174x215",174,215)
        (self.img_btn_bg_4_data,self.img_btn_bg_4_dsc) = self.get_icon("img_btn_bg_4_174x215",174,215)
        
        (self.img_copy_data,self.img_copy_dsc) = self.get_icon("img_copy_51x60",51,60)
        (self.img_print_data,self.img_print_dsc) = self.get_icon("img_print_65x64",65,64)
        (self.img_scan_data,self.img_scan_dsc) = self.get_icon("img_scan_51x61",51,61)
        (self.img_setup_data,self.img_setup_dsc) = self.get_icon("img_setup_63x64",63,64)
        
        (self.img_usb_data,self.img_usb_dsc) = self.get_icon("img_usb_62x61",62,61)
        (self.img_internet_data,self.img_internet_dsc) = self.get_icon("img_internet_65x64",65,64)
        (self.img_mobile_data,self.img_mobile_dsc) = self.get_icon("img_mobile_50x60",50,60)
        (self.img_wave_data,self.img_wave_dsc) = self.get_icon("img_wave_27x47",27,47)
        (self.img_phone_data,self.img_phone_dsc) = self.get_icon("img_phone_77x99",77,99)
        
        (self.img_ready,self.img_ready_dsc) = self.get_icon("img_ready_158x158",158,158)
        
        (self.img_printer2_data,self.img_printer2_dsc)       = self.get_icon("img_printer2_107x104",107,104)
        (self.img_no_internet_data,self.img_no_internet_dsc) = self.get_icon("img_no_internet_42x42",42,42)
        (self.img_cloud_data,self.img_cloud_dsc)             = self.get_icon("img_cloud_93x59",93,59)
        
        (self.scan_example_data,self.scan_example_dsc) = self.get_icon("scan_example_522x340",522,340)
        self.theme = Theme()

        self.home_open(0)

    def home_open(self,delay):
        
        self.bg_top.set_style_local_bg_opa(lv.obj.PART.MAIN, lv.STATE.DEFAULT,lv.OPA.COVER)
        self.bg_top.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.DEFAULT,LV_DEMO_PRINTER_BLUE)
        self.bg_top.set_y(self.LV_DEMO_PRINTER_BG_NORMAL)

        self.cont = lv.cont(lv.scr_act(),None)
        self.cont.set_size(350,80)
        self.cont.clean_style_list(lv.cont.PART.MAIN)
        self.cont.align(None, lv.ALIGN.IN_TOP_LEFT, 60, 0)
        
        icon = lv.img(self.cont, None)
        icon.set_src(self.icon_wifi_dsc)
        icon.align(None, lv.ALIGN.IN_TOP_LEFT, 20, 45)
        self.anim_in(icon, delay);

        icon = lv.img(self.cont, None)
        icon.set_src(self.icon_tel_dsc)
        icon.align(None, lv.ALIGN.IN_TOP_LEFT, 110, 45)
        self.anim_in(icon, delay);

        icon = lv.img(self.cont, None)
        icon.set_src(self.icon_eco_dsc)
        icon.align(None, lv.ALIGN.IN_TOP_LEFT, 200, 45)
        self.anim_in(icon, delay);

        icon = lv.img(self.cont, None)
        icon.set_src(self.icon_pc_dsc)
        icon.align(None, lv.ALIGN.IN_TOP_LEFT, 290, 45)
        self.anim_in(icon, delay);

        title = self.add_title("23 February 2021 20:13");
        title.align(None, lv.ALIGN.IN_TOP_RIGHT, -60, LV_DEMO_PRINTER_TITLE_PAD)
        
        delay += self.LV_DEMO_PRINTER_ANIM_DELAY
        self.anim_in(title, delay)
        
        box_w = 720;
        box = lv.obj(lv.scr_act(), None)
        box.set_size(box_w, 260)
        self.theme.apply(box,lv.THEME.CONT)
        
        box.align(None, lv.ALIGN.IN_TOP_MID, 0, 100)

        delay += self.LV_DEMO_PRINTER_ANIM_DELAY
        self.anim_in(box, delay)
        
        icon = self.add_icon(box, self.img_btn_bg_1_dsc, self.img_copy_dsc, "COPY")
        icon.align(None, lv.ALIGN.IN_LEFT_MID, 1 * (box_w - 20) // 8 - 80, 0)
        icon.set_event_cb(self.copy_open_icon_event_cb)
        icon.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME * 2, delay + self.LV_DEMO_PRINTER_ANIM_TIME + 50)
        
        icon = self.add_icon(box, self.img_btn_bg_2_dsc, self.img_scan_dsc, "SCAN")
        icon.align(None, lv.ALIGN.IN_LEFT_MID, 3 * (box_w - 20) // 8 - 80, 0)
        icon.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME * 2, delay + self.LV_DEMO_PRINTER_ANIM_TIME + 50)
        icon.set_event_cb(self.scan_open_icon_event_cb)
        
        icon = self.add_icon(box, self.img_btn_bg_3_dsc, self.img_print_dsc, "PRINT")
        icon.align(None, lv.ALIGN.IN_LEFT_MID, 5 * (box_w - 20) // 8 - 80, 0)
        icon.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME * 2, delay + self.LV_DEMO_PRINTER_ANIM_TIME + 50)
        icon.set_event_cb(self.print_open_event_cb);

        icon = self.add_icon(box, self.img_btn_bg_4_dsc, self.img_setup_dsc, "SETUP");
        icon.align(None, lv.ALIGN.IN_LEFT_MID, 7 * (box_w - 20) // 8 - 80, 0)
        icon.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME * 2, delay + self.LV_DEMO_PRINTER_ANIM_TIME + 50)
        icon.set_event_cb(self.setup_icon_event_cb)

        box = lv.obj(lv.scr_act(), None)
        box.set_size(500, 80)
        box.align(None, lv.ALIGN.IN_BOTTOM_LEFT, self.LV_HOR_RES // 20,
                     - self.LV_HOR_RES // 40)
        label = lv.label(box,None)
        label.set_text("What do you want to do today?")
        self.theme.apply(label,lv.THEME.LABEL)
        label.align(box,lv.ALIGN.CENTER,0,0)
    
        delay += self.LV_DEMO_PRINTER_ANIM_DELAY;
        self.anim_in(box,delay)
        
        box = lv.obj(lv.scr_act(), None)
        box_w = 200;
        box.set_size(box_w, 80)
        box.align(None, lv.ALIGN.IN_BOTTOM_RIGHT, - self.LV_HOR_RES // 20,
                     - self.LV_HOR_RES // 40)
        
        bar = lv.bar(box, None)
        bar.set_style_local_bg_color(lv.bar.PART.INDIC, lv.STATE.DEFAULT,
                                        lv.color_hex(0x01d3d4))
        bar.set_size(25, 50)
        bar.align(None, lv.ALIGN.IN_LEFT_MID, 1 * (box_w - 20) // 8 + 10, 0)
        bar.set_value(60, lv.ANIM.ON)

        bar = lv.bar(box, None)
        bar.set_style_local_bg_color(lv.bar.PART.INDIC, lv.STATE.DEFAULT,
                                        lv.color_hex(0xe600e6))
        bar.set_size(25, 50)
        bar.align(None, lv.ALIGN.IN_LEFT_MID, 3 * (box_w - 20) // 8 + 10, 0)
        bar.set_value(30, lv.ANIM.ON)
        
        bar = lv.bar(box, None)
        bar.set_style_local_bg_color(lv.bar.PART.INDIC, lv.STATE.DEFAULT,
                                     lv.color_hex(0xefef01))
        bar.set_size(25, 50)
        bar.align(None, lv.ALIGN.IN_LEFT_MID, 5 * (box_w - 20) // 8 + 10, 0)
        bar.set_value(80, lv.ANIM.ON)
        
        bar = lv.bar(box, None)
        bar.set_style_local_bg_color(lv.bar.PART.INDIC, lv.STATE.DEFAULT,
                                        lv.color_hex(0x1d1d25))
        bar.set_size(25, 50)
        bar.align(None, lv.ALIGN.IN_LEFT_MID, 7 * (box_w - 20) // 8 + 10, 0)
        bar.set_value(20, lv.ANIM.ON)
    #
    # get an icon
    #
    def get_icon(self,filename,xres,yres):

        try:
            sdl_filename = 'images/' + filename + "_argb8888.bin"
            self.log.debug('sdl filename: ' + sdl_filename)
            with open(sdl_filename,'rb') as f:
                icon_data = f.read()
                self.log.debug(sdl_filename + " successfully read")
        except:
            self.log.error("Could not find image file: " + filename) 
            return None
        
        icon_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": xres, "h": yres, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data": icon_data,
                "data_size": len(icon_data),
            }
        )
        return (icon_data,icon_dsc) 

    def add_title(self,txt):
        title = lv.label(lv.scr_act(), None)
        self.theme.apply(title,LV_DEMO_PRINTER_THEME_TITLE)
        title.set_text(txt)
        title.align(None, lv.ALIGN.IN_TOP_MID, 0, LV_DEMO_PRINTER_TITLE_PAD)
        return title

    def add_icon(self,parent,src_bg_dsc,src_icon_dsc,txt):
        bg = lv.img(parent,None)
        bg.set_click(True)
        bg.set_src(src_bg_dsc)
        self.theme.apply(bg,LV_DEMO_PRINTER_THEME_ICON)
        bg.set_antialias(False)

        icon = lv.img(bg,None)
        icon.set_src(src_icon_dsc)
        icon.set_style_local_image_recolor_opa(lv.img.PART.MAIN, lv.STATE.DEFAULT, lv.OPA.TRANSP)
        icon.align(None, lv.ALIGN.IN_TOP_RIGHT, -30, 30)

        label = lv.label(bg,None)
        label.set_text(txt)
        label.align(None, lv.ALIGN.IN_BOTTOM_LEFT, 30, -30)
        self.theme.apply(label,lv.THEME.LABEL)
        return bg
                
    def copy_open_icon_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.anim_out_all(lv.scr_act(), 0)
            self.log.debug("copy_open_icon_event_cb")
            self.scan_btn_txt = "NEXT"
            delay = 200
            self.anim_bg(150, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_FULL)

            arc = self.add_loader(self.scan_anim_ready)
            arc.align(None, lv.ALIGN.CENTER, 0, -40)
            txt = lv.label(lv.scr_act(), None)
            txt.set_text("Scanning, please wait...")
            self.theme.apply(txt, LV_DEMO_PRINTER_THEME_LABEL_WHITE)
            txt.align(arc, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)

            self.anim_in(arc, delay);
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(txt, delay);
    
            self.icon_generic_event_cb(obj, evt)
            
    def scan_open_icon_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("scan_open_icon_event_cb")
            self.scan_btn_txt = "SAVE"
            self.anim_out_all(lv.scr_act(), 0)
            delay = 200
            self.anim_bg(150, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_FULL);
            arc = self.add_loader(self.scan_anim_ready)
            arc.align(None, lv.ALIGN.CENTER, 0, -40)

            txt = lv.label(lv.scr_act(), None)
            txt.set_text("Scanning, please wait...");
            self.theme.apply(txt, LV_DEMO_PRINTER_THEME_LABEL_WHITE)
            txt.align(arc, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)

            self.anim_in(arc, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(txt, delay)

    def print_open_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.anim_out_all(lv.scr_act(), 0)
            self.print_open(200)
            self.icon_generic_event_cb(obj,evt)

    def print_open(self,delay):
        back = self.add_back(self.back_to_home_event_cb)
        self.anim_in(back,delay)

        title = self.add_title("PRINT MENU")

        box_w = 720
        box = lv.obj(lv.scr_act(), None)
        box.set_size(box_w, 260)
        box.align(None,lv.ALIGN.IN_TOP_MID, 0, 100)
        
        delay += self.LV_DEMO_PRINTER_ANIM_DELAY;
        self.anim_in(box, delay)

        icon = self.add_icon(box, self.img_btn_bg_2_dsc, self.img_usb_dsc, "USB");
        icon.align(None, lv.ALIGN.IN_LEFT_MID, 1 * box_w // 7 -40, 0)
        icon.set_event_cb(self.usb_icon_event_cb)
        icon.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME * 2, delay + self.LV_DEMO_PRINTER_ANIM_TIME + 50)
        
        icon = self.add_icon(box, self.img_btn_bg_3_dsc, self.img_mobile_dsc, "MOBILE");
        icon.align(None, lv.ALIGN.IN_LEFT_MID, 3 * box_w // 7 -40, 0)
        icon.set_event_cb(self.mobile_icon_event_cb)
        icon.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME * 2, delay + self.LV_DEMO_PRINTER_ANIM_TIME + 50)

        icon = self.add_icon(box, self.img_btn_bg_4_dsc, self.img_internet_dsc, "INTERNET");
        icon.align(None, lv.ALIGN.IN_LEFT_MID, 5 * box_w // 7 -40, 0)
        icon.set_event_cb(self.internet_icon_event_cb)
        icon.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME * 2, delay + self.LV_DEMO_PRINTER_ANIM_TIME + 50)

        box = lv.obj(lv.scr_act(), None)
        box.set_size(box_w, 80);
        box.align(None, lv.ALIGN.IN_BOTTOM_LEFT, self.LV_HOR_RES // 20,
            - self.LV_HOR_RES // 40);
        label = lv.label(box,None)
        self.theme.apply(label,lv.THEME.LABEL)
        label.set_text("From where do you want to print?")
        label.align(box,lv.ALIGN.CENTER,0,0)

        delay += self.LV_DEMO_PRINTER_ANIM_DELAY;
        self.anim_in(box, delay)

        self.anim_bg(0, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_NORMAL);       
        
    def icon_generic_event_cb(self,obj,evt):
        if evt == lv.EVENT.PRESSED:
            img = obj.get_child_back(None)
            txt = obj.get_child(None)
            self.log.debug("icon_generic_event")
            
            a = lv.anim_t()
            a.init()
            a.set_time(100)

            a.set_var(img)
            a.set_custom_exec_cb(lambda a, val: self.set_x(img,val))
            # a.set_custom_exec_cb(lv_obj_set_x)
            a.set_values(img.get_x(), obj.get_width() - img.get_width() - 35)
            lv.anim_t.start(a)

            # a.set_custom_exec_cb(&a, (lv_anim_exec_xcb_t)lv_obj_set_y);
            a.set_custom_exec_cb(lambda a, val: self.set_y(img,val))
            a.set_values(img.get_y(), 35)
            lv.anim_t.start(a)

            a.set_var(txt)
            a.set_custom_exec_cb(lambda a, val: self.set_x(txt,val))
            a.set_values(txt.get_x(), 35)
            lv.anim_t.start(a)


            a.set_custom_exec_cb(lambda a, val: self.set_y(txt,val))
            a.set_values(txt.get_y(), obj.get_height() - txt.get_height() -35)
            lv.anim_t.start(a)
        
    def setup_icon_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("setup_icon_event_cb")
            self.anim_out_all(lv.scr_act(), 0)
            
            self.anim_bg(0, LV_DEMO_PRINTER_RED, self.LV_DEMO_PRINTER_BG_FULL)
            delay = 200
            
            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_printer2_dsc);
            img.align(None, lv.ALIGN.CENTER, -90, 0)

            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY        
            
            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_no_internet_dsc)
            img.align(None, lv.ALIGN.CENTER, 0, -40)
            
            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY   
            
            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_cloud_dsc)
            img.align(None, lv.ALIGN.CENTER, 80, -80)
            
            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY

            self.info_bottom_create("You have no permission to change the settings.", "BACK", self.back_to_home_event_cb, delay)
                        
    def add_loader(self, end_cb):
        arc = lv.arc(lv.scr_act(),None)
        arc.set_bg_angles(0, 0)
        arc.set_start_angle(270)
        arc.set_size(220, 220)
        self.theme.apply(arc,lv.THEME.ARC)        
        self.log.debug("Starting loader anim")
        a = lv.anim_t()
        a.init()
        a.set_custom_exec_cb(lambda a, val: self.loader_anim_cb(a,arc,val))
        a.set_values(0, 110)
        a.set_time(2000)
        a.set_ready_cb(end_cb)
        lv.anim_t.start(a)                

        return arc

    def loader_anim_cb(self,a,arc,v):
        # self.log.debug("loader_anim_cb called with value: %d"%v)
        if v > 100:
            v = 100
        arc.set_end_angle(v * 360 // 100 + 270)
        percent_txt = "%d %%"%v
        arc.set_style_local_value_str(lv.arc.PART.BG, lv.STATE.DEFAULT, percent_txt)

                                     
    def anim_in(self,obj,delay):
        a = lv.anim_t()
        a.init()
        a.set_var(obj)
        a.set_time(self.LV_DEMO_PRINTER_ANIM_TIME)
        a.set_delay(delay)
        # a.set_exec_cb(obj.set_y)
        # a.set_values(obj.get_y() -  self.LV_DEMO_PRINTER_ANIM_Y, obj.get_y())
        # a.start()
        obj.fade_in(self.LV_DEMO_PRINTER_ANIM_TIME - 50, delay)

    def anim_out_all(self,obj,delay):
        self.log.debug("anim_out_all")
        child = obj.get_child_back(None)
        while child:
            if child != self.scan_img and child != self.bg_top and child != self.bg_bottom and child != lv.scr_act():
                a = lv.anim_t()
                a.init()
                a.set_var(child)
                a.set_time(self.LV_DEMO_PRINTER_ANIM_TIME)
                # a.set_exec_cb(lambda y: lv.obj.set_y(y))
                if child.get_y() < 80:
                    a.set_values(child.get_y(),child.get_y() - self.LV_DEMO_PRINTER_ANIM_Y)
                else:
                    a.set_values(child.get_y(),child.get_y() + self.LV_DEMO_PRINTER_ANIM_Y)
                    delay += self.LV_DEMO_PRINTER_ANIM_DELAY
                a.set_ready_cb(lv.obj.del_anim_ready_cb)
                lv.anim_t.start(a)
            child = obj.get_child_back(child)                   
        
    def scan_anim_ready(self,a):
        self.log.debug("scan_anim_ready")
        self.anim_out_all(lv.scr_act(), 0)
        self.scan1_open(self.scan_btn_txt)
        
    def scan1_open(self,btn_txt):
        self.log.debug("scan1_open " + btn_txt)
        self.anim_out_all(lv.scr_act(), 0)
        
        self.anim_bg(0, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_NORMAL)
        delay = 200
        back = self.add_back(self.back_to_home_event_cb)
        title = self.add_title("ADJUST IMAGE")

        self.scan_img = lv.img(lv.scr_act(), None)
        self.scan_img.set_src(self.scan_example_dsc)
        self.scan_img.align(None, lv.ALIGN.IN_TOP_LEFT, 40, 100)
        self.scan_img.set_style_local_radius(lv.img.PART.MAIN, lv.STATE.DEFAULT, 10)
        self.scan_img.set_style_local_clip_corner(lv.img.PART.MAIN, lv.STATE.DEFAULT, True)
        self.scan_img.set_style_local_image_recolor_opa(lv.img.PART.MAIN, lv.STATE.DEFAULT, 80)
        
        box_w = 160
        settings_box = lv.obj(lv.scr_act(), None)
        settings_box.set_size(box_w, 245)
        settings_box.align(self.scan_img, lv.ALIGN.OUT_RIGHT_TOP, 40, 0)

        self.lightness_act = 0
        self.hue_act = 180

        slider = lv.slider(settings_box, None)
        slider.set_size(8, 160)
        slider.align(None, lv.ALIGN.IN_TOP_MID, - 35, 65)
        slider.set_event_cb(self.lightness_slider_event_cb)
        slider.set_range(-80, 80)
        slider.set_value(0, lv.ANIM.OFF)
        slider.set_ext_click_area(30, 30, 30, 30)
        self.theme.apply(slider,lv.THEME.SLIDER)
            
        icon = lv.img(settings_box, None)
        icon.set_src(self.icon_bright_dsc)
        icon.align(slider, lv.ALIGN.OUT_TOP_MID, 0, -30)
        
        slider = lv.slider(settings_box, slider)
        slider.align(None, lv.ALIGN.IN_TOP_MID, 35, 65)
        slider.set_event_cb(self.hue_slider_event_cb)
        slider.set_range(0, 359)
        slider.set_value(180, lv.ANIM.OFF)
        self.theme.apply(slider,lv.THEME.SLIDER)
        
        icon = lv.img(settings_box, None)
        icon.set_src(self.icon_hue_dsc)
        icon.align(slider, lv.ALIGN.OUT_TOP_MID, 0, -30)

        self.scan_img_color_refr();

        next_btn = lv.btn(lv.scr_act(), None)
        self.theme.apply(next_btn, LV_DEMO_PRINTER_THEME_BTN_CIRCLE)
        next_btn.set_size(box_w, 60)
        next_btn.align(self.scan_img, lv.ALIGN.OUT_RIGHT_BOTTOM, 40, 0)
        if btn_txt == "NEXT":
            next_btn.set_event_cb(self.scan_next_event_cb)
            next_btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "NEXT")
            next_btn.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
        elif btn_txt == "SAVE":
            next_btn.set_event_cb(self.scan_save_event_cb)
            next_btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "SAVE")
            next_btn.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            next_btn.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.DEFAULT, LV_DEMO_PRINTER_GREEN)
            next_btn.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.PRESSED, LV_DEMO_PRINTER_GREEN.color_darken(lv.OPA._20))

    def scan_save_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.scan_img = None

            self.anim_out_all(lv.scr_act(), 0)
            self.anim_bg(0, LV_DEMO_PRINTER_GREEN, self.LV_DEMO_PRINTER_BG_FULL)

            delay = 200

            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_ready_dsc);
            img.align(None, lv.ALIGN.CENTER, 0, -40)

            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(img, delay)

            self.info_bottom_create("File saved", "CONTINUE", self.back_to_home_event_cb, delay)
            
    def scan_next_event_cb(self,obj,evt):
        LV_IMG_ZOOM_NONE = 250
        if evt == lv.EVENT.CLICKED:
            self.anim_out_all(lv.scr_act(), 0)

            delay = 400

            back = self.add_back(self.back_to_home_event_cb)
            self.anim_in(back, delay)

            title = self.add_title("ADJUST IMAGE")
            self.anim_in(title, delay)

            box_w = 400
            self.scan_img.set_pivot(0, 0)
            self.scan_img.set_antialias(False)

            a = lv.anim_t()
            a.init()
            a.set_var(self.scan_img)
            a.set_custom_exec_cb(lambda a,val: self.set_zoom(self.scan_img,val))
            a.set_values(LV_IMG_ZOOM_NONE, 190)
            a.set_time(200)
            a.set_delay(200)
            lv.anim_t.start(a)

            # self.scan_img = None    # To allow anim out

            dropdown_box = lv.obj(lv.scr_act(), None)
            dropdown_box.set_size(box_w, self.LV_VER_RES // 5)
            dropdown_box.align(None, lv.ALIGN.IN_BOTTOM_LEFT, 40, -20)

            dropdown = lv.dropdown(dropdown_box, None)
            dropdown.align(None, lv.ALIGN.IN_LEFT_MID, self.LV_HOR_RES // 60, 0)
            dropdown.set_max_height(self.LV_VER_RES // 3)
            dropdown.set_options_static("Best\nNormal\nDraft")
            dropdown.set_width((box_w - 3 * self.LV_HOR_RES // 60) // 2)
            self.theme.apply(dropdown,lv.THEME.DROPDOWN)
            
            dropdown = lv.dropdown(dropdown_box, dropdown)
            dropdown.align(None, lv.ALIGN.IN_RIGHT_MID, - self.LV_HOR_RES // 60, 0)
            dropdown.set_options_static("72 DPI\n96 DPI\n150 DPI\n300 DPI\n600 DPI\n900 DPI\n1200 DPI")
            self.theme.apply(dropdown,lv.THEME.DROPDOWN)
            
            box_w = 320 - 40
            settings_box = lv.obj(lv.scr_act(), None)
            settings_box.set_size(box_w, self.LV_VER_RES // 2)
            settings_box.align(None, lv.ALIGN.IN_TOP_RIGHT, -40, 100)

            numbox = lv.cont(settings_box, None)
            self.theme.apply(numbox, LV_DEMO_PRINTER_THEME_BOX_BORDER)
            numbox.set_size(self.LV_HOR_RES // 7, self.LV_HOR_RES // 13)
            numbox.align(settings_box, lv.ALIGN.IN_TOP_MID, 0, self.LV_VER_RES // 10)
            numbox.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "Copies")
            numbox.set_style_local_value_align(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
            numbox.set_style_local_value_ofs_y(lv.obj.PART.MAIN, lv.STATE.DEFAULT, - self.LV_VER_RES // 50)
            numbox.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            numbox.set_layout(lv.LAYOUT.CENTER)

            self.print_cnt = 1
            self.print_cnt_label = lv.label(numbox, None)
            self.print_cnt_label.set_text("1")
            self.print_cnt_label.set_style_local_text_font(lv.label.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())

            btn = lv.btn(settings_box, None)
            btn.set_size(self.LV_HOR_RES // 13, self.LV_HOR_RES // 13)
            btn.align(numbox, lv.ALIGN.OUT_LEFT_MID, - self.LV_VER_RES // 60, 0)
            btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.DOWN)
            btn.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            btn.set_event_cb(self.print_cnt_btn_event_cb)
            btn.set_ext_click_area(10, 10, 10, 10);
            self.theme.apply(btn,lv.THEME.BTN)
            
            sw = lv.switch(settings_box, None)
            sw.set_size(self.LV_HOR_RES // 10, self.LV_VER_RES // 12)
            sw.align(btn, lv.ALIGN.OUT_BOTTOM_LEFT, self.LV_HOR_RES // 50, self.LV_VER_RES // 7)
            sw.set_style_local_value_ofs_y(lv.obj.PART.MAIN, lv.STATE.DEFAULT, - self.LV_VER_RES // 50)
            sw.set_style_local_value_align(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
            sw.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "Color")
            sw.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            self.theme.apply(sw,lv.THEME.SWITCH)
            
            btn = lv.btn(settings_box, btn)
            btn.align(numbox, lv.ALIGN.OUT_RIGHT_MID, self.LV_VER_RES // 60, 0)
            btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.UP)
            btn.set_event_cb(self.print_cnt_btn_event_cb)
            self.theme.apply(btn,lv.THEME.BTN)
            
            sw = lv.switch(settings_box, sw)
            sw.align(btn, lv.ALIGN.OUT_BOTTOM_RIGHT, - self.LV_HOR_RES // 50, self.LV_VER_RES // 7)
            sw.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "Vertical")

            print_btn = lv.btn(lv.scr_act(), None)
            self.theme.apply(print_btn, LV_DEMO_PRINTER_THEME_BTN_CIRCLE)
            print_btn.set_size(box_w, 60)
            print_btn.set_event_cb(self.print_start_event_cb)
            
            btn_ofs_y = (dropdown_box.get_height() - print_btn.get_height()) // 2
            print_btn.align(settings_box, lv.ALIGN.OUT_BOTTOM_MID, 0, self.LV_HOR_RES // 30 + btn_ofs_y)
            print_btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "PRINT")
            print_btn.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            print_btn.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.DEFAULT, LV_DEMO_PRINTER_GREEN)
            print_btn.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.PRESSED, LV_DEMO_PRINTER_GREEN.color_darken(lv.OPA._20))

            delay += self.LV_DEMO_PRINTER_ANIM_DELAY;
            self.anim_in(settings_box, delay)

            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(dropdown_box, delay)

            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(print_btn, delay)

            self.anim_bg(0, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_NORMAL)
            
    def anim_bg(self,delay,color,y_new):
        self.log.debug("anim_bg: new y: %d"%y_new)
        y_act = self.bg_top.get_y()
        act_color = self.bg_top.get_style_bg_color(lv.obj.PART.MAIN)
        self.log.debug("current y: %d"%y_act)
        if y_new != self.LV_DEMO_PRINTER_BG_NORMAL and y_new == y_act and  act_color.full == color.full:
            return
        
        if (y_new == self.LV_DEMO_PRINTER_BG_NORMAL and y_new == y_act) or \
           (y_new == self.LV_DEMO_PRINTER_BG_NORMAL and y_act == self.LV_DEMO_PRINTER_BG_FULL):            
            path = lv.anim_path_t()
            path.init()
            path.set_cb(self.triangle_path_cb)
            
            a = lv.anim_t()
            a.set_var(self.bg_top)
            a.set_time(self.LV_DEMO_PRINTER_ANIM_TIME_BG + 200)
            a.set_delay(delay)
            a.set_custom_exec_cb(lambda a, val: self.set_y(self.bg_top,val))
            a.set_values(y_act, y_new)
            a.set_path(path)
            lv.anim_t.start(a)
        else:
            a = lv.anim_t()
            a.set_var(self.bg_top)
            a.set_time(self.LV_DEMO_PRINTER_ANIM_TIME_BG)
            a.set_delay(delay)
            a.set_custom_exec_cb(lambda a, val: self.set_y(self.bg_top,val))
            a.set_values(self.bg_top.get_y(), y_new)
            lv.anim_t.start(a)

        color_anim = lv.anim_t()
        self.bg_color_prev = self.bg_color_act
        self.bg_color_act = color
        color_anim.set_custom_exec_cb(lambda color_anim, val: self.anim_bg_color_cb(val))
        color_anim.set_values(0, 255)
        color_anim.set_time(self.LV_DEMO_PRINTER_ANIM_TIME_BG)
        path = lv.anim_path_t()
        path.init()
        path.set_cb(lv.anim_path_t.linear)
        # a.set_path(lv.anim_t.path_def)
        lv.anim_t.start(color_anim)

    def triangle_path_cb(self,path,a):
        if a.time == a.act_time:
            return a.end
        if a.act_time < a.time//2:
            step = a.act_time * 1024 // (a.time//2)
            new_value = step * self.LV_DEMO_PRINTER_BG_SMALL - a.start
            new_value >>= 10
            new_value += a.start
            self.log.debug("triangle: new value: %d"%new_value)
            return new_value
        else:
            t = a.act_time - a.time // 2
            step = a.act_time * 1024 // (a.time//2)
            new_value = step * (a.end - self.LV_DEMO_PRINTER_BG_SMALL) 
            new_value >>= 10
            new_value += self.LV_DEMO_PRINTER_BG_SMALL
            self.log.debug("triangle: new value: %d"%new_value)
            return new_value        
        
    def set_y(self,obj,new_y):
        self.log.debug("Setting y to %d"%new_y)
        obj.set_y(new_y)
        
    def set_x(self,obj,new_x):
        self.log.debug("Setting x to %d"%new_x)
        obj.set_x(new_x)
                                 
    def set_zoom(self,obj,new_size):
        self.log.debug("Setting zoom to %d"%new_size)
        obj.set_zoom(new_size)
                                 
    def anim_bg_color_cb(self,v):
        self.log.debug("anim_bg_color_cb: Mixing colors with value: %d"%v)
        c = self.bg_color_act.color_mix(self.bg_color_prev,v)
        self.bg_top.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.DEFAULT, c)
        
    def info_bottom_create(self, label_txt, btn_txt, btn_event_cb, delay):
        LV_DEMO_PRINTER_BTN_W = 200
        LV_DEMO_PRINTER_BTN_H =  50
        
        txt = lv.label(lv.scr_act(), None)
        txt.set_text(label_txt)
        self.theme.apply(txt,LV_DEMO_PRINTER_THEME_LABEL_WHITE)
        txt.align(None,lv.ALIGN.CENTER, 0, 100)

        btn = lv.btn(lv.scr_act(), None)
        self.theme.apply(btn,LV_DEMO_PRINTER_THEME_BTN_BORDER)
        btn.set_size(LV_DEMO_PRINTER_BTN_W,LV_DEMO_PRINTER_BTN_H)
        btn.align(txt, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)
        
        btn.set_style_local_value_str(lv.btn.PART.MAIN, lv.STATE.DEFAULT, btn_txt)
        btn.set_style_local_value_font(lv.btn.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_normal())
        btn.set_event_cb(btn_event_cb)
        
        self.anim_in(txt, delay)
        delay += self.LV_DEMO_PRINTER_ANIM_DELAY;
        
        self.anim_in(btn, delay);
        delay += self.LV_DEMO_PRINTER_ANIM_DELAY;
        
        self.anim_in(btn, delay);        

    def back_to_home_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.scan_img=None
            self.anim_out_all(lv.scr_act(), 0)
            self.home_open(200)
        pass

    def add_back(self,event_cb):
        btn = lv.btn(lv.scr_act(), None)
        self.theme.apply(btn,LV_DEMO_PRINTER_THEME_BTN_BACK)
        btn.set_size(80,80)
        btn.set_pos(30,10)
        btn.set_event_cb(event_cb)
        return btn

    def lightness_slider_event_cb(self,obj,evt):
        if evt == lv.EVENT.VALUE_CHANGED:
            self.lightness_act = obj.get_value()
            self.log.debug("lightness_slider_event: new slider value: %d"%self.lightness_act)
            self.scan_img_color_refr();
    
    def hue_slider_event_cb(self,obj,evt):
        if evt == lv.EVENT.VALUE_CHANGED:
            self.hue_act = obj.get_value()
            self.log.debug("hue_slider_event: new slider value: %d"%self.hue_act)
            self.scan_img_color_refr();
        
    def scan_img_color_refr(self):
        if self.lightness_act > 0:
            s = 100 - self.lightness_act
            v = 100
        else:
            s = 100
            v = 100 + self.lightness_act
        self.log.debug("scan_img_color_refr: hue, s, v: %d %d %d"%(self.hue_act,s,v))
        
        c = lv.color_hsv_to_rgb(self.hue_act,s,v)
        self.scan_img.set_style_local_image_recolor(lv.img.PART.MAIN, lv.STATE.DEFAULT, c)

    def internet_icon_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.anim_out_all(lv.scr_act(),0)
            self.anim_bg(0, LV_DEMO_PRINTER_RED, self.LV_DEMO_PRINTER_BG_FULL);

            delay = 200

            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_printer2_dsc)
            img.align(None, lv.ALIGN.CENTER, -90, 0)

            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY

            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_no_internet_dsc)
            img.align(None, lv.ALIGN.CENTER, 0, -40)

            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY

            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_cloud_dsc)
            img.align(None, lv.ALIGN.CENTER, 80, -80)

            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY

            self.info_bottom_create("No internet connection", "BACK", self.back_to_print_event_cb, delay)
    
        self.icon_generic_event_cb(obj, evt)

    def mobile_icon_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.anim_out_all(lv.scr_act(), 0)

            self.anim_bg(0, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_FULL);

            delay = 200;

            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_printer2_dsc)
            img.align(None, lv.ALIGN.CENTER, -90, 0)

            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY

            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_wave_dsc)
            img.align(None, lv.ALIGN.CENTER, 0, 0)

            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY

            img = lv.img(lv.scr_act(), None)
            img.set_src(self.img_phone_dsc)
            img.align(None, lv.ALIGN.CENTER, 80, 0)

            self.anim_in(img, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY

            self.info_bottom_create("Put you phone near to the printer", "BACK", self.back_to_print_event_cb, delay)
            
        self.icon_generic_event_cb(obj, evt)

    def usb_icon_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.anim_out_all(lv.scr_act(), 0)

            delay = 200

            back = self.add_back(self.back_to_print_event_cb)
            self.anim_in(back, delay)

            title = self.add_title("PRINTING FROM USB DRIVE")
            self.anim_in(title, delay)

            box_w = self.LV_HOR_RES * 5 // 10
            list = lv.list(lv.scr_act(), None)
            list.set_size(box_w, self.LV_VER_RES // 2);
            list.align(None, lv.ALIGN.IN_TOP_LEFT, self.LV_HOR_RES // 20, self.LV_VER_RES // 5)
            
            dummy_file_list = ["Contract 12.pdf", "Scanned_05_21.pdf", "Photo_132210.jpg", "Photo_232141.jpg",
                 "Photo_091640.jpg", "Photo_124019.jpg", "Photo_232032.jpg", "Photo_232033.jpg", "Photo_232034.jpg",
                 "Monday schedule.pdf", "Email from John.txt", "New file.txt", "Untitled.txt", "Untitled (1).txt",
                 "Gallery_40.jpg","Gallery_41.jpg", "Gallery_42.jpg", "Gallery_43.jpg", "Gallery_44.jpg"]
            
            for filename in dummy_file_list:
                btn = lv.btn.__cast__(list.add_btn(lv.SYMBOL.FILE, filename))
                btn.set_checkable(True)
                self.theme.apply(btn,lv.THEME.LIST_BTN)

            dropdown_box = lv.obj(lv.scr_act(), None)
            dropdown_box.set_size(box_w, self.LV_VER_RES // 5);
            dropdown_box.align(list, lv.ALIGN.OUT_BOTTOM_MID, 0, self.LV_HOR_RES // 30)

            dropdown = lv.dropdown(dropdown_box, None)
            dropdown.align(None, lv.ALIGN.IN_LEFT_MID, self.LV_HOR_RES // 60, 0)
            dropdown.set_max_height(self.LV_VER_RES // 3)
            dropdown.set_options_static("Best\nNormal\nDraft")
            dropdown.set_width((box_w - 3 * self.LV_HOR_RES // 60) // 2)
            dropdown.set_ext_click_area(5, 5, 5, 5)
            self.theme.apply(dropdown,lv.THEME.DROPDOWN)
                
            dropdown = lv.dropdown(dropdown_box, dropdown)
            dropdown.align(None, lv.ALIGN.IN_RIGHT_MID, - self.LV_HOR_RES // 60, 0)
            # dropdown.set_options_static("100 DPI\n200 DPI\n300 DPI\n400 DPI\n500 DPI\n1500 DPI")
            dropdown.set_options_static("\n".join([
                "100 DPI","200 DPI","300 DPI","400 DPI","500 DPI","1500 DPI"]))
            self.theme.apply(dropdown,lv.THEME.DROPDOWN)
            
            box_w = 320 - 40;
            settings_box = lv.obj(lv.scr_act(), None)
            settings_box.set_size(box_w, self.LV_VER_RES // 2);
            settings_box.align(list, lv.ALIGN.OUT_RIGHT_TOP, self.LV_HOR_RES // 20, 0)

            self.print_cnt = 1
            numbox = lv.cont(settings_box, None)
            self.theme.apply(numbox, LV_DEMO_PRINTER_THEME_BOX_BORDER)
            numbox.set_size(self.LV_HOR_RES // 7, self.LV_HOR_RES // 13)
            numbox.align(settings_box, lv.ALIGN.IN_TOP_MID, 0, self.LV_VER_RES // 10)
            numbox.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "Copies")
            numbox.set_style_local_value_align(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
            numbox.set_style_local_value_ofs_y(lv.obj.PART.MAIN, lv.STATE.DEFAULT, - self.LV_VER_RES // 50)
            numbox.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            numbox.set_layout(lv.LAYOUT.CENTER)

            self.print_cnt_label = lv.label(numbox, None)
            self.print_cnt_label.set_text("1")
            self.print_cnt_label.set_style_local_text_font(lv.label.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            

            btn = lv.btn(settings_box, None)
            btn.set_size(self.LV_HOR_RES // 13, self.LV_HOR_RES // 13)
            btn.align(numbox, lv.ALIGN.OUT_LEFT_MID, - self.LV_VER_RES // 60, 0)
            btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.DOWN)
            btn.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            btn.set_event_cb(self.print_cnt_btn_event_cb)
            btn.set_ext_click_area(10, 10, 10, 10)
            self.theme.apply(btn,lv.THEME.BTN)
            
            sw = lv.switch(settings_box, None)
            sw.set_size(self.LV_HOR_RES // 10, self.LV_VER_RES // 12)
            sw.align(btn, lv.ALIGN.OUT_BOTTOM_LEFT, self.LV_HOR_RES // 50, self.LV_VER_RES // 7)
            sw.set_style_local_value_ofs_y(lv.obj.PART.MAIN, lv.STATE.DEFAULT, - self.LV_VER_RES // 50)
            sw.set_style_local_value_align(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.ALIGN.OUT_TOP_MID)
            sw.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "Color")
            sw.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            self.theme.apply(sw,lv.THEME.SWITCH)

            btn = lv.btn(settings_box, btn)
            btn.align(numbox, lv.ALIGN.OUT_RIGHT_MID, self.LV_VER_RES // 60, 0)
            btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, lv.SYMBOL.UP)
            btn.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())            
            self.theme.apply(btn,lv.THEME.BTN)
            btn.set_event_cb(self.print_cnt_btn_event_cb)
                          
            sw = lv.switch(settings_box, sw)
            sw.align(btn, lv.ALIGN.OUT_BOTTOM_RIGHT, - self.LV_HOR_RES // 50, self.LV_VER_RES // 7)
            sw.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "Vertical")
            self.theme.apply(sw,lv.THEME.SWITCH)
            
            print_btn = lv.btn(lv.scr_act(), None)
            self.theme.apply(print_btn, LV_DEMO_PRINTER_THEME_BTN_CIRCLE)
            print_btn.set_size(box_w, 60)

            btn_ofs_y = (dropdown_box.get_height() - print_btn.get_height()) // 2
            print_btn.align(settings_box, lv.ALIGN.OUT_BOTTOM_MID, 0, self.LV_HOR_RES // 30 + btn_ofs_y)
            print_btn.set_style_local_value_str(lv.obj.PART.MAIN, lv.STATE.DEFAULT, "PRINT")
            print_btn.set_style_local_value_font(lv.obj.PART.MAIN, lv.STATE.DEFAULT, self.theme.get_font_subtitle())
            print_btn.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.DEFAULT, LV_DEMO_PRINTER_GREEN)
            print_btn.set_style_local_bg_color(lv.obj.PART.MAIN, lv.STATE.PRESSED, LV_DEMO_PRINTER_GREEN.color_darken(lv.OPA._20))
            print_btn.set_event_cb(self.print_start_event_cb)

            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(list, delay);

            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(settings_box, delay)

            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(dropdown_box, delay);
            
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(print_btn, delay)
            
            self.anim_bg(0, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_NORMAL)

    def print_cnt_btn_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED or evt == lv.EVENT.LONG_PRESSED_REPEAT: 
        # if evt == lv.EVENT.CLICKED:
            txt = obj.get_style_value_str(lv.btn.PART.MAIN)
            if txt == lv.SYMBOL.DOWN:
                if self.print_cnt > 1:
                    self.print_cnt -= 1
            else:
                if self.print_cnt < 1000:
                    self.print_cnt +=1
                    
            self.print_cnt_label.set_text(str(self.print_cnt))

    def print_start_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.scan_img = None
            self.anim_out_all(lv.scr_act(), 0)
            delay = 200
            self.anim_bg(150, LV_DEMO_PRINTER_BLUE, self.LV_DEMO_PRINTER_BG_FULL)
            
            arc = self.add_loader(lambda a: self.print_start_ready())
            arc.align(None, lv.ALIGN.CENTER, 0, -40)
            
            txt = lv.label(lv.scr_act(), None)
            txt.set_text("Printing, please wait...")
            self.theme.apply(txt,LV_DEMO_PRINTER_THEME_LABEL_WHITE)
            txt.align(arc, lv.ALIGN.OUT_BOTTOM_MID, 0, 60)

            self.anim_in(arc, delay)
            delay += self.LV_DEMO_PRINTER_ANIM_DELAY
            self.anim_in(txt, delay)

    def print_start_ready(self):
        self.anim_bg(0, LV_DEMO_PRINTER_GREEN, self.LV_DEMO_PRINTER_BG_FULL)
        self.anim_out_all(lv.scr_act(), 0);
        
        img = lv.img(lv.scr_act(), None)
        img.set_src(self.img_ready_dsc)
        img.align(None, lv.ALIGN.CENTER, 0, -40)
        
        delay = 200
        self.anim_in(img, delay)
        delay += self.LV_DEMO_PRINTER_ANIM_DELAY

        self.info_bottom_create("Printing finished", "CONTINUE", self.back_to_home_event_cb, delay)
        
    def back_to_print_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.anim_out_all(lv.scr_act(), 0)
            self.print_open(150)
        
drv = driver(width=800,height=480,orientation=ORIENT_LANDSCAPE)
printer = DemoPrinter()
