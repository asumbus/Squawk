# Version 5.0 - Now with less but more YAY!!

from gps import *
import os
import time
import threading
import math
import utm
import datetime
from stops import *


class GpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE)  # starting the stream of info
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False

    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc

    @property
    def satellites(self):
        return self.gpsd.satellites

# function so that heading goes back to 0 form 360.
def between(head, low, high):
    """Whether the heading head is between headings low and high."""
    head, low, high = map(lambda x: x % 360, (head, low, high))
    if high >= low:
        return low <= head <= high
    return low <= head < 360 or 0 <= head <= high


# set Flags all off to start with.
flag = False

# set to something to start with.
s = 1
track = 1

# heading Error set 15 degrees
headerror = 15

# tracking function

def tracker(stop_north, stop_east, stop_heading, circle_size, delay_time, stop_name, mp3):
    global flag
    if (((north - stop_north) ** 2) + ((east - stop_east) ** 2) <= (circle_size ** 2) and
            between(gpsc.fix.track, stop_heading - headerror, stop_heading + headerror)):
        while not flag:
            print "Arriving at", stop_name
            #os.system('mpg321 -q /home/pi/Desktop/GPS/audio/'+mp3+'.mp3')
            print mp3
            flag = True
            time.sleep(delay_time)
            break
        else:
            print "Still inside", stop_name
            time.sleep(delay_time)
    else:
        flag = False
        return



if __name__ == '__main__':
    # create the controller
    gpsc = GpsController()
    try:
        # start controller
        gpsc.start()
        print "Starting"
        while True:
            status = gpsc.fix.mode
            speed = (gpsc.fix.speed * 2.2369)


            if status <= 1:
                print "Searching for GPS Fix"
                time.sleep(60)
            else:
                north, east, zone, band = utm.from_latlon(gpsc.fix.latitude, gpsc.fix.longitude)
                track = (north, east, gpsc.fix.latitude, gpsc.fix.longitude, gpsc.fix.track,
                         speed, gpsc.fix.epx, gpsc.fix.epy, gpsc.utc)

                # print track
                s = str(track)

                for stop in busstops:
                    tracker(*busstops[stop])

                #################################################################
                # PSA #
                # Edit in #

                gpsdate = datetime.datetime.strptime(gpsc.utc, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.timedelta(hours=7)

                if date1 <= gpsdate <= date2:
                    for psa in busstops:
                        tracker(*psastops[psa])
                else:
                    pass

            time.sleep(0.3)

    # Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    finally:
        print "Stopping gps controller"
        gpsc.stopController()
        # wait for the tread to finish
        gpsc.join()

    print "Done"
