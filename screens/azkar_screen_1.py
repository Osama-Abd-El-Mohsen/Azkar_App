from kivy.factory import Factory as F
from utils import load_kv_path
from kivy.clock import Clock
load_kv_path("screens/azkar_screen_1.kv")


class AzkarScreen_1(F.Screen):
    def on_pre_enter(self, *args):
        print("-"*50)
        print(self)
        print("-"*50)
        # parent_manager = self.parent
        # if 'Loading Screen' not in parent_manager.screen_names:
        #     parent_manager.add_widget(self.get_screen_object_from_screen_name('Loading Screen'))
        # parent_manager.current = 'Loading Screen'


    def get_screen_object_from_screen_name(self, screen_name):
        screen_module_in_str = "_".join([i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())
        exec(f"from screens.{screen_module_in_str} import {screen_object_in_str}")
        screen_object = eval(f"{screen_object_in_str}()")
        return screen_object

