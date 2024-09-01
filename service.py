from time import sleep
from kivy.clock import Clock
import datetime ,time
from kivy import platform
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

if platform == 'android':
    from notification import MyAndroidNotification
    from jnius import autoclass
    notificator = MyAndroidNotification()


now = datetime.datetime.now().time()
start = datetime.time(16, 45)
end = datetime.time(18)

def check_medical_appointments(*args):
    print("="*50)
    print (start <= now <= end)
    print("="*50)
    if start <= now <= end:
        if platform == 'android':
            notificator.notify(
                app_name="Azkary",
                title="افتكرى",
                message="متنسيش تقرئى اذكار المساء 😊",
                app_icon=f"Assets/icon/FFAFED.ico",
                ticker="ticker test",
                toast=False
            )

        MediaPlayer = autoclass('android.media.MediaPlayer')
        AudioManager = autoclass('android.media.AudioManager')
        mPlayer = MediaPlayer()
        mPlayer.setDataSource('azkar.wav')
        mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
        mPlayer.prepare()
        mPlayer.start()

if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    Clock.schedule_interval(check_medical_appointments,5*60)
    # while True:
    #     check_medical_appointments()
    #     sleep(5*60)
