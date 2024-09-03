from kivy.factory import Factory as F
from utils import load_kv_path

load_kv_path("screens/loading_screen.kv")

class LoadingScreen(F.Screen):
    parent1=''
    state = 0 
    def on_pre_enter(self):
        if self.state == 0:
            self.parent1 = self.parent
            self.state = 1

        print(self.parent1)
        if 'Main Screen' not in self.parent1.screen_names:
            self.parent1.add_widget(self.get_screen_object_from_screen_name('Main Screen'))

    def on_enter(self):
        self.parent1.current = 'Main Screen'


    def get_screen_object_from_screen_name(self, screen_name):
        screen_module_in_str = "_".join([i.lower() for i in screen_name.split()])
        screen_object_in_str = "".join(screen_name.split())
        exec(f"from screens.{screen_module_in_str} import {screen_object_in_str}")
        screen_object = eval(f"{screen_object_in_str}()")
        return screen_object