from kivymd.app import MDApp
from kivymd.utils.set_bars_colors import set_bars_colors
import webbrowser
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemSupportingText
from kivymd.uix.dialog import *
from kivymd.uix.button import MDButton, MDButtonText, MDButtonIcon
from kivy.uix.screenmanager import SlideTransition, WipeTransition, ScreenManager, Screen, NoTransition
from kivy.uix.widget import Widget
from kivy import platform
from kivy.clock import Clock
from oscpy.client import OSCClient
from oscpy.server import OSCThreadServer
import pandas as pd
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from functools import partial
from kivy.core.text import LabelBase
from kivy.core.window import Window
if platform != "android":
    Window.size = (406, 762)
    Window.always_on_top = True
import datetime
Window.clearcolor = (16/255, 19/255, 24/255, 1)

class MyScreenManager(ScreenManager):
    pass


class MainApp(MDApp):
    azkar_data = pd.read_csv('azkar.csv', index_col=0)
    zekr_list = []
    description_list = []
    count_list = []
    reference_list = []

    def set_bars_colors(self):
        set_bars_colors(
            [22/255, 26/255, 29/255,1],
            [16/255, 19/255, 24/255,1],
            "Light"
        )
####################### Helper Functions #########################
    def go_main(self):
        self.root.transition = WipeTransition()
        self.root.current = 'Main Screen'

    def get_cat_data(self, row):
        for index, field in enumerate(row.index):
            if index == 1:
                self.zekr_list.append(row[field])
            elif index == 2:
                self.description_list.append(row[field])
            elif index == 3:
                self.count_list.append(row[field])
            elif index == 4:
                self.reference_list.append(row[field])

    def calculate_card_height(self, zekr, desc):
        base_height = 150 
        zekr_height = dp(20) + len(zekr) * dp(0.5)
        desc_height = dp(20) + len(desc) * dp(0.5)
        total_height = base_height + zekr_height + desc_height
        return total_height

    def generate_azkar(self):
        for zekr, desc, self.count, ref in zip(self.zekr_list, self.description_list, self.count_list, self.reference_list):
            yield zekr,desc,self.count,ref

    def counter_func(self):
        counter_btn = self.screen_manager.get_screen('Azkar Screen_1').ids['counter']
        self.counter+=1
        if self.counter < float(self.count) :
            counter_btn.text = str(self.counter) + '/' + f'{float(self.count):0.0f}'
        elif self.counter == float(self.count):
            counter_btn.text = str(self.counter) + '/' + f'{float(self.count):0.0f}'
            self.display_next()

    def restart_generator(self):
        self.zekr_list = []
        self.description_list = []
        self.count_list = []
        self.reference_list = []
        self.start_generator()

    def start_generator(self):
        self.counter = 0
        self.current_item_index = -1
        self.generator = self.generate_azkar()

    def change_label(self):
        label = self.screen_manager.get_screen('Azkar Screen_1').ids['label']
        label.text = str(self.current_item_index+1) + '/' + str(len(self.cat_data))

    def display_current(self):
        try:
            self.change_label() 
            counter_btn = self.screen_manager.get_screen('Azkar Screen_1').ids['counter']
            self.counter = 0
            zekr, desc, self.count, ref = next(self.generator)

            counter_btn.text = str(self.counter) + '/' + f'{float(self.count):0.0f}'
            self.screen_manager.get_screen('Azkar Screen_1').ids['list'].clear_widgets()
            self.add_zekr_card(zekr,desc,self.count,ref)

        except StopIteration:
            print("No more items to display")

    def display_prev(self):
        try:
            if self.current_item_index > 0:
                self.current_item_index -= 1  
                self.generator = self.generate_azkar()
                for _ in range(self.current_item_index):
                    next(self.generator)  
                self.display_current() 
            else:
                if self.current_item_index < 0:
                    self.current_item_index = 0
                print("No previous item")
        except StopIteration:
            print("No more items to display")

    def display_next(self):
        try:
            counter_btn = self.screen_manager.get_screen('Azkar Screen_1').ids['counter']
            self.counter = 0
            zekr, desc, self.count, ref = next(self.generator)
            counter_btn.text = str(self.counter) + '/' + f'{float(self.count):0.0f}'
            self.screen_manager.get_screen('Azkar Screen_1').ids['list'].clear_widgets()
            self.add_zekr_card(zekr,desc,self.count,ref)
            self.current_item_index += 1 
            self.change_label() 

        except StopIteration:
            print("End of list")

    def add_zekr_card(self,zekr,desc,count,ref):
        self.screen_manager.get_screen('Azkar Screen_1').ids['list'].clear_widgets()
        if len(desc) != 1:
            self.screen_manager.get_screen('Azkar Screen_1').ids['list'].add_widget(
                MDCard(
                    MDBoxLayout(
                        MDBoxLayout(
                            MDLabel(
                                text=f"{zekr}",
                                theme_text_color="Custom",
                                theme_font_name="Custom",
                                theme_font_size="Custom",
                                font_name="BBCairo",
                                text_color="#f4f9fc",
                                font_script_name="Arab",
                                font_size=dp(15),
                                halign='center',
                                font_direction="rtl",
                            ),
                            orientation='horizontal',
                            # md_bg_color="#789987",

                        ),
                        MDBoxLayout(
                            MDLabel(
                                text=f"{desc}",
                                theme_text_color="Custom",
                                theme_font_name="Custom",
                                theme_font_size="Custom",
                                font_name="BBCairo",
                                text_color="#11ac68",
                                font_size=dp(12),
                                halign='center',
                                font_script_name="Arab",
                                font_direction="rtl",
                            ),
                            orientation='horizontal',
                            # md_bg_color="#789987",
                            size_hint=(1, None),
                        ),

                        MDBoxLayout(
                            MDBoxLayout(
                                MDLabel(
                                    text=f"{ref}" if len(
                                        ref) != 1 else "لا يوجد",
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    font_script_name="Arab",
                                    font_direction="rtl",
                                    text_color="#c2c6c9",
                                    font_size=dp(12),
                                ),
                                MDLabel(
                                    text=f"المصدر : ",
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    font_script_name="Arab",
                                    font_direction="rtl",
                                    text_color="#11ac68",
                                    font_size=dp(12),
                                ),
                                orientation='horizontal',
                                size_hint=(1, .2),
                                pos_hint={"left": 1},
                            ),
                            MDBoxLayout(
                                MDLabel(
                                    text=f"{int(float(count))}",
                                    halign='left',
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    text_color="#c2c6c9",
                                    font_size=dp(12),
                                ),
                                MDLabel(
                                    text=f"عدد المرات : ",
                                    halign='left',
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    font_script_name="Arab",
                                    font_direction="rtl",
                                    text_color="#11ac68",
                                    font_size=dp(12),
                                ),
                                orientation='horizontal',
                                size_hint=(.4, .2),

                            ),
                            orientation='horizontal',
                            # md_bg_color="#789987",
                            size_hint_y=0.1
                        ),
                        orientation='vertical',
                        padding=dp(5),
                        spacing=dp(5),

                    ),
                    style="elevated",
                    pos_hint={"center_x": .5, "center_y": .5},
                    theme_bg_color="Custom",
                    md_bg_color="#161a1d",
                    theme_shadow_softness="Custom",
                    shadow_softness=15,
                    theme_elevation_level="Custom",
                    elevation_level=1,
                    size_hint=(.5, None),
                    padding=(10, 10, 10, 10),
                    state_hover=0,
                    state_press=0,
                    radius=(15,15,15,15),
                    height=self.calculate_card_height(zekr, desc)
                ),
            )
        else :
            self.screen_manager.get_screen('Azkar Screen_1').ids['list'].add_widget(
                MDCard(
                    MDBoxLayout(
                        MDBoxLayout(
                            MDLabel(
                                text=f"{zekr}",
                                theme_text_color="Custom",
                                theme_font_name="Custom",
                                theme_font_size="Custom",
                                font_name="BBCairo",
                                text_color="#f4f9fc",
                                font_script_name="Arab",
                                font_size=dp(15),
                                halign='center',
                                font_direction="rtl",
                            ),
                            orientation='horizontal',
                            # md_bg_color="#789987",

                        ),
                        MDBoxLayout(
                            MDLabel(
                                text=f"{desc}",
                                theme_text_color="Custom",
                                theme_font_name="Custom",
                                theme_font_size="Custom",
                                font_name="BBCairo",
                                text_color="#11ac68",
                                font_size=dp(12),
                                halign='center',
                                font_script_name="Arab",
                                font_direction="rtl",
                            ),
                            orientation='horizontal',
                            # md_bg_color="#789987",
                            size_hint=(1, None),
                        ),

                        MDBoxLayout(
                            MDBoxLayout(
                                MDLabel(
                                    text=f"{ref}" if len(
                                        ref) != 1 else "لا يوجد",
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    font_script_name="Arab",
                                    font_direction="rtl",
                                    text_color="#c2c6c9",
                                    font_size=dp(12),
                                ),
                                MDLabel(
                                    text=f"المصدر : ",
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    font_script_name="Arab",
                                    font_direction="rtl",
                                    text_color="#11ac68",
                                    font_size=dp(12),
                                ),
                                orientation='horizontal',
                                size_hint=(1, .2),
                                pos_hint={"left": 1},
                            ),
                            MDBoxLayout(
                                MDLabel(
                                    text=f"{int(float(self.count))}",
                                    halign='left',
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    text_color="#c2c6c9",
                                    font_size=dp(12),
                                ),
                                MDLabel(
                                    text=f"عدد المرات : ",
                                    halign='left',
                                    adaptive_size=True,
                                    theme_text_color="Custom",
                                    theme_font_name="Custom",
                                    theme_font_size="Custom",
                                    font_name="BBCairo",
                                    font_script_name="Arab",
                                    font_direction="rtl",
                                    text_color="#11ac68",
                                    font_size=dp(12),
                                ),
                                orientation='horizontal',
                                size_hint=(.4, .2),

                            ),
                            orientation='horizontal',
                            # md_bg_color="#789987",
                            size_hint_y=0.1
                        ),
                        orientation='vertical',
                        padding=dp(5),
                        spacing=dp(5),

                    ),
                    style="elevated",
                    pos_hint={"center_x": .5, "center_y": .5},
                    theme_bg_color="Custom",
                    md_bg_color="#161a1d",
                    theme_shadow_softness="Custom",
                    shadow_softness=15,
                    theme_elevation_level="Custom",
                    elevation_level=1,
                    size_hint=(.5, None),
                    padding=(10, 10, 10, 10),
                    state_hover=0,
                    state_press=0,
                    radius=(15,15,15,15),
                    height=self.calculate_card_height(zekr, desc)
                ),
            )
        fab = self.screen_manager.get_screen('Azkar Screen_1').ids['fab']
        counter = self.screen_manager.get_screen('Azkar Screen_1').ids['counter']
        if self.count == 0 :
            print("in zero")
            fab.opacity= 0.0
            counter.text=''
            counter.text_color = '#101318'
        else :
            counter.text_color = '#161a1d'
            fab.opacity= 1.0
        

    def make_cats(self):
        # self.screen_manager.transition = WipeTransition()
        # self.screen_manager.current = 'Loading Screen'
        cats = self.azkar_data['category'].unique()
        for cat in cats : 
            if cat != "أذكار الصباح":
                self.screen_manager.get_screen('Main Screen').ids['list'].add_widget(
                    MDCard(
                        MDButtonIcon(
                            icon= "mosque",
                            theme_icon_color= "Custom",
                            theme_bg_color= "Custom",
                            theme_font_size= "Custom",
                            md_bg_color= "#161a1d",
                            icon_color= "#11ac68" ,
                            font_size= dp(16),
                            size= ("16dp", "16dp"),
                        ),
                        MDBoxLayout(
                            MDLabel(
                                text=cat,
                                theme_text_color="Custom",
                                theme_font_name="Custom",
                                theme_font_size="Custom",
                                font_name="BBCairo",
                                text_color="#f4f9fc",
                                font_script_name="Arab",
                                font_size=dp(16),
                                halign='right',
                                font_direction="rtl",
                            ),
                            orientation='horizontal',
                            # md_bg_color="#789987",
                            adaptive_height = True,
                            pos_hint= {"center_x": .5,"center_y": .5},

                        ),

                        style="elevated",
                        pos_hint={"center_x": .5, "center_y": .5},
                        theme_bg_color="Custom",
                        md_bg_color="#161a1d",
                        padding=(20, 20, 20, 20),
                        state_hover=0,
                        state_press=0,
                        radius=(15,15,15,15),
                        on_press=partial(self.get_azkar,cat),
                        size_hint=(1, None),
                        height=dp(70),

                )
            )

    def get_azkar(self, zekr_cat: str,*args):
        self.restart_generator()
        # self.screen_manager.transition = WipeTransition()
        # self.screen_manager.current = 'Loading Screen'
        self.cat_data = self.azkar_data[self.azkar_data.category == zekr_cat]
        self.cat_data.apply(self.get_cat_data, axis=1)
        self.display_next()
        self.screen_manager.current = 'Azkar Screen_1'


####################### Android Service ##########################
    def andoid_start_service(name, other_arg):
        from android import mActivity
        from jnius import autoclass
        context = mActivity.getApplicationContext()
        service_name = "org.me.azkar" + ".Service" + "Azkar"
        service = autoclass(service_name)
        service.start(mActivity, '')  # starts or re-initializes a service
        return service
####################### Android Service ##########################

####################### Build App Function #######################
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.Android_back_click)

    def Android_back_click(self,window,key,*largs):
        if key in [27, 1001]:
            self.root.transition = WipeTransition()
            self.root.current = 'Main Screen'
            return True

    def build(self):
        self.screen_manager = MyScreenManager()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        self.screen_manager.add_widget(self.get_screen_object_from_screen_name('Loading Screen'))
        self.screen_manager.current = 'Loading Screen'
        self.make_cats()
        return self.screen_manager

    def get_screen_object_from_screen_name(self, screen_name):
        screen_module_in_str = "_".join(
            [i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())
        exec(
            f"from screens.{screen_module_in_str} import {screen_object_in_str}")
        screen_object = eval(f"{screen_object_in_str}()")
        
        return screen_object

    def on_start(self):
        def callback(permission, results):
            if all([res for res in results]):
                Clock.schedule_once(self.set_dynamic_color)
                
        super().on_start()

        if platform == "android":
            from android.permissions import Permission, request_permissions
            permissions = [Permission.POST_NOTIFICATIONS, Permission.READ_EXTERNAL_STORAGE,Permission.WRITE_EXTERNAL_STORAGE, Permission.FOREGROUND_SERVICE]
            request_permissions(permissions, callback)

            self.service = self.andoid_start_service('Azkar')
            print(f'started android service. {self.service}')

        elif platform in ('linux', 'linux2', 'macos', 'win'):
            print("="*50)
            print(platform)
            print("="*50)
            from runpy import run_path
            from threading import Thread
            self.service = Thread(
                target=run_path,
                args=['./service.py'],
                kwargs={'run_name': '__main__'},
                daemon=True
            )
            self.service.start()

        else:
            raise NotImplementedError(
                "service start not implemented on this platform"
            )
####################### Events Function ##########################


####################### Info Dialog ##############################

    def info_dialog(self):
        self.InfoDialog = MDDialog(
            MDDialogIcon(
                icon="information",
                theme_icon_color="Custom",
                icon_color="#11ac68"
            ),
            MDDialogHeadlineText(
                text="About App",
                theme_text_color="Custom",
                theme_font_name="Custom",
                theme_font_size="Custom",
                font_name="BPoppins",
                text_color="#f4f9fc",
                font_size=dp(18),
            ),
            MDDialogSupportingText(
                text="this app devolped by Osama Abd El Mohsen".capitalize(),
                halign='center',
                theme_text_color="Custom",
                theme_font_name="Custom",
                theme_font_size="Custom",
                font_name="MPoppins",
                text_color="#f4f9fc",
                font_size=dp(13),
            ),

            MDDialogContentContainer(
                MDDivider(color="#11ac68"),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="gmail",
                        theme_icon_color="Custom",
                        icon_color="#11ac68"
                    ),
                    MDListItemSupportingText(
                        text="Osama.m.abdelmohsen@gmail.com",
                        theme_text_color="Custom",
                        theme_font_name="Custom",
                        theme_font_size="Custom",
                        font_name="MPoppins",
                        text_color="#f4f9fc",
                        font_size=dp(10),
                    ),
                    on_press=self.info_email_link,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDListItem(
                    MDListItemLeadingIcon(
                        icon="github",
                        theme_icon_color="Custom",
                        icon_color="#11ac68"
                    ),
                    MDListItemSupportingText(
                        text="Osama-Abd-El-Mohsen",
                        theme_text_color="Custom",
                        theme_font_name="Custom",
                        theme_font_size="Custom",
                        font_name="MPoppins",
                        text_color="#f4f9fc",
                        font_size=dp(10),

                    ),
                    on_press=self.info_github_link,
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ),
                MDDivider(color="#11ac68"),
                orientation="vertical",
            ),

            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(
                        text="Ok",
                        theme_text_color="Custom",
                        theme_font_name="Custom",
                        theme_font_size="Custom",
                        font_name="BPoppins",
                        text_color="#f4f9fc",
                        font_size=dp(13),
                    ),
                    style="tonal",
                    theme_bg_color="Custom",
                    md_bg_color="#101318",
                    on_press=self.close_info_dialog
                ),

                spacing="8dp",
            ),
            id="infodialog",
            theme_bg_color="Custom",
            _md_bg_color="#161a1d",
            state_hover=0,
            state_press=0,
        )
        self.InfoDialog.open()

    def close_info_dialog(self, *args):
        self.InfoDialog.dismiss()

    def info_github_link(self, *arg):
        webbrowser.open("http://www.github.com/Osama-Abd-El-Mohsen")

    def info_email_link(self, *arg):
        webbrowser.open("mailto:Osama.m.abdelmohsen@gmail.com")

    def bug_report_link(self, *arg):
        webbrowser.open("https://forms.gle/kcvaGvwxjow2mRS37")
####################### Info Dialog ##############################


####################### Main ####################################
if __name__ == "__main__":
    LabelBase.register(name="BBCairo", fn_regular="font/cairo/Cairo-Black.ttf")
    LabelBase.register(
        name="BPoppins", fn_regular="font/Poppins/Poppins-Bold.ttf")
    LabelBase.register(
        name="MPoppins", fn_regular="font/Poppins/Poppins-Medium.ttf")

    MainApp().run()
####################### Main ####################################
