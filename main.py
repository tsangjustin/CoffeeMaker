import twitter
import time
from datetime import datetime
import RPi.GPIO as GPIO

api = twitter.Api(consumer_key=consumer_key,
                      consumer_secret=consumer_secret,
                      access_token_key=access_token_key,
                      access_token_secret=access_token_secret)
GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.HIGH)

def StartAlarm():
    GPIO.output(11, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(11, GPIO.LOW)

''''''''''''''''''''''''''''''''''''''''''''''''''''''
# Pre: Function takes number of cups of coffee to make
# Peri: Function turns on GPIO at pin 13 for numCups *
#       120 seconds. Turns off pin 13 after sleep
# Post: returns nothing

''''''''''''''''''''''''''''''''''''''''''''''''''''''
def StartBrew(numCups):
    # Turn GPIO output on/1
    GPIO.output(13, GPIO.LOW)
    time.sleep(120 * numCups)
    # Turn GPIO output off/0
    GPIO.output(13, GPIO.HIGH)

def DMBack():
    api.PostDirectMessage("IEEEcoffeemaker", "Coffee is done")

def MakeCoffee():
    timeline = api.GetUserTimeline('IEEEcoffeemaker')
    tweet = timeline[0].text.split()

    # Read most recent post on timeline
    if tweet[0] == '#coffeetime':
        print "Retrieving Time..."
        # Parse tweet to get end time
        hour = float(tweet[1][0:2])
        minute = float(tweet[1][3:5])
        numCups = float(tweet[2])
        # Get the current time
        curr_now = datetime.now()
        str_now = curr_now.strftime("%H:%M")
        now_hour = (float(str_now[0:2]) - 5.0) % 24.0
        now_min = float(str_now[3:5])
        # Find the difference from end - current time
        diff_hour = int(hour - now_hour) % 24
        diff_min = int(minute - now_min) % 60
        if (now_min > minute):
            diff_hour = diff_hour - 1
        if numCups <= 0:
            numCups = 1
        diff_time = (diff_hour * 3600) + (diff_min * 60)
        print diff_time
        time.sleep(diff_time - 5)
        StartAlarm()
        StartBrew(numCups)
        DMBack()
    else:
        print "No coffee, :( waiting..."

if __name__ == '__main__':
    while True:
        print "Starting..."
        MakeCoffee()
        GPIO.cleanup
