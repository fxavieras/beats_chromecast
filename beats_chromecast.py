from time import sleep
import atexit
import schedule #pip -- task scheduler
import pychromecast #pip -- chromecast controls in python
import keyboard
from pychromecast.controllers.youtube import YouTubeController

print("init beats_chromecast -- hello!")
yt = YouTubeController()                                #init youtube handler out here for scope

wake_time = ""                                          #init wake_time string for scope - is this the right way to do this in python?


def beats():                                            #connects to chromecast, opens the player and plays the stream
    try:                                                #catch errors connecting to chromecast. chromecast may be off.
        pychromecast.discover_chromecasts()             #connect to chromecast
        chromecasts, delist_variable = pychromecast.get_listed_chromecasts(friendly_names = ["Cellar TV"])  #delist_variable exists so this returns a "Chromecast" object rather than a list element  
        cast = chromecasts[0]
        cast.wait()

        cast.register_handler(yt)                       #assign youtube handler to chromecast and play stream
        yt.play_video("5qap5aO4i9A")
    
    except:                                             #if error, try again
        print("chromecast error. retrying...")
        beats()

    print("working")
    
    print('\n' +"Welcome to Beats to Wake up/Relax to.... Enjoy your morning :)")
    print("Pour yourself a cup of coffee and take a deep breath..." + '\n')
    atexit.register(cast.quit_app)  #debug - closes youtube player when python script is closed

    for i in range(30):                                 #volume fade in
        cast.set_volume(i/30)
        sleep(1)

    for i in range(3600):                               #1 hour
        if keyboard.is_pressed('esc'):
            break
        sleep(1)
    cast.quit_app()
    print("stopping")


def set_time():                                         #sets alarm time
    global wake_time
    wake_time = input("What time would you like to wake up?" + '\n')

    if len(wake_time) == 4:                             #fix AM H:MM formats without "0" in front
        wake_time = "0" + wake_time
    
    print("Alarm will start at " + wake_time)
    print('\n' + "Press escape at any time to reset alarm." + '\n')
    scheduling()                                        #updates scheduler with new alarm time


def scheduling():                                       #updates scheduler with new wake_time info
    try:                                                #catches bad-format strings (non HH:MM)
        global wake_time
        schedule.every().day.at(wake_time).do(beats)
    except:
        print("Something went wrong scheduling the alarm. Please try again.")  #this is usually a bad user input
        set_time()


set_time()  #on startup

while True:                                             #checks for tasks every 1s
    schedule.run_pending()
    sleep(1)
    if keyboard.is_pressed('esc'):                    #if space is pressed, reset alarm time
        set_time()