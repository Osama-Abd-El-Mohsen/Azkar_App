from time import sleep
import datetime 
from kivy.clock import Clock
from kivy import platform
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient

if platform == 'android':
    print("in android")
    from notification import MyAndroidNotification
    from jnius import autoclass
    notificator = MyAndroidNotification()


start = datetime.time(16, 45)
end = datetime.time(18)

def send_reminder(*args):
    now = datetime.datetime.now().time()
    print("="*50)
    print (start <= now <= end)
    print("="*50)
    if start <= now <= end:
        try :
            notificator.notify(
                app_name="Azkary",
                title="افتكرى",
                message="متنسيش تقرئى اذكار المساء 😊",
                app_icon=f"Assets/ico.ico",
                ticker="ticker test",
                toast=False
            )
        except Exception as e:
            print(f"Notification Error: {e}")

        try:
            MediaPlayer = autoclass('android.media.MediaPlayer')
            AudioManager = autoclass('android.media.AudioManager')
            mPlayer = MediaPlayer()
            mPlayer.setDataSource('azkar.wav')
            mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
            mPlayer.prepare()
            mPlayer.start()
        except Exception as e:
            print(f"Media Player Error: {e}")

if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=3000, default=True)
    # Clock.schedule_interval(send_reminder,5*60)
    while True:
        print("before while")
        send_reminder()
        sleep(5*60)