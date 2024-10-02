from time import sleep
import datetime 
from kivy import platform
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
import requests
from kivy.storage.jsonstore import JsonStore

if platform == 'android':
    print("in android")
    from notification import MyAndroidNotification
    from jnius import autoclass
    notificator = MyAndroidNotification()

online_state = 0
asr_target_time = 0
sunrise_target_time = 0
stored_data = JsonStore('data.json')
asr_time = "16:27"
sunrise_time = "06:33"
elmoulk_time = datetime.time(22, 0)
added_time = datetime.timedelta(minutes=15)
def get_prayer_times():
    try:
        url = f'http://api.aladhan.com/v1/timingsByCity?city=talkha&country=egypt&method=5'
        response = requests.get(url)
        info = response.json()

        if 'data' in info:
            timings = info['data']['timings']
            return timings
    except Exception as e :
        print(e)


def load_from_JSON():
    global asr_time,sunrise_time,online_state
    asr_time = stored_data.get('time1')['asr']
    sunrise_time = stored_data.get('time')['sunrise']
    online_state = stored_data.get('online')['state']
    print("-"*50 +"\n"+"From Load")
    print(asr_time)
    print(sunrise_time)
    print(online_state)
    print("-"*50 )

def save_to_JSON():
    stored_data.put('time1', asr=asr_time)
    stored_data.put('time', sunrise=sunrise_time)
    stored_data.put('online', state=online_state)

save_to_JSON()


def update_prayer_times():
    global asr_target_time,sunrise_target_time,online_state
    load_from_JSON()
    try :
        if online_state == 0 :
            global asr_time,sunrise_time
            timings = get_prayer_times()
            sunrise_time = timings['Sunrise']
            asr_time = timings['Asr']
            online_state = 1
            save_to_JSON()
            print("="*50+"\n"+"From get_prayer_times (online)")
            print(asr_time)
            print(sunrise_time)
            print(online_state)
            print("="*50)
    except Exception as e :
        print(e)

    try:
        hour,min = asr_time.split(':')
        hour1,min1 = sunrise_time.split(':')
        # asr_target_time = datetime.time(int(hour), int(min))
        asr_target_time = (datetime.datetime.combine(datetime.date.today(), datetime.time(int(hour), int(min))) + added_time).time()

        sunrise_target_time = datetime.time(int(hour1), int(min1))

    except Exception as e: 
        print(e)
    
def send_reminder(*args):
    update_prayer_times()
    print(f"asr_target_time = {asr_target_time}")
    print(f"sunrise_target_time = {sunrise_target_time}")
    now = datetime.datetime.now().time().replace(microsecond=0)
    print("="*50)
    print(now)
    print(asr_target_time)
    print(sunrise_target_time)
    print(elmoulk_time)
    print (asr_target_time == now)
    print (sunrise_target_time == now)
    print (elmoulk_time == now)
    print("="*50)

    if asr_target_time == now :
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

        # try:
        #     MediaPlayer = autoclass('android.media.MediaPlayer')
        #     AudioManager = autoclass('android.media.AudioManager')
        #     mPlayer = MediaPlayer()
        #     mPlayer.setDataSource('azkar.wav')
        #     mPlayer.setAudioStreamType(AudioManager.STREAM_NOTIFICATION)
        #     mPlayer.prepare()
        #     mPlayer.start()
        # except Exception as e:
        #     print(f"Media Player Error: {e}")

    elif sunrise_target_time == now :
        try :
            notificator.notify(
                app_name="Azkary",
                title="افتكرى",
                message="متنسيش تقرئى اذكار الصباح 😊",
                app_icon=f"Assets/ico.ico",
                ticker="ticker test",
                toast=False
            )
        except Exception as e:
            print(f"Notification Error: {e}")

    elif elmoulk_time == now :
        try :
            notificator.notify(
                app_name="Azkary",
                title="افتكرى",
                message="متنسيش تقرئى سورة الملك 😊",
                app_icon=f"Assets/ico.ico",
                ticker="ticker test",
                toast=False
            )
        except Exception as e:
            print(f"Notification Error: {e}")


if __name__ == '__main__':
    SERVER = OSCThreadServer()
    SERVER.listen('localhost', port=2002, default=True)
    # Clock.schedule_interval(send_reminder, 1)
    while True:
        print("before while")
        send_reminder()
        sleep(1)