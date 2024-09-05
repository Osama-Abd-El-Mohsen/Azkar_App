from kivy.factory import Factory as F
from utils import load_kv_path
from kivy.clock import Clock
load_kv_path("screens/azkar_screen_1.kv")


class AzkarScreen_1(F.Screen):
    def on_pre_enter(self, *args):
        pass