# Version 4.0 - Now with PSA YAY!

from gps import *
import os
import time
import threading
import math
import utm
import datetime


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

def tracker(stop_north, stop_east, stop_heading, circle_size, stop_name, mp3):
    global flag
    if (((north - stop_north) ** 2) + ((east - stop_east) ** 2) <= (circle_size ** 2) and
            between(gpsc.fix.track, stop_heading - headerror, stop_heading + headerror)):
        while not flag:
            print "Arriving at", stop_name
            #f.write('\nArriving at' '' + stop_name + '')
            os.system('mpg321 -q /home/pi/Desktop/GPS/audio/'+mp3+'.mp3')
            flag = True
            time.sleep(60)
            break
        else:
            print "Still inside", stop_name
            #f.write('\nStill inside' '' + stop_name + '')
            time.sleep(60)
    else:
        flag = False
        return



if __name__ == '__main__':
    # create the controller
    gpsc = GpsController()
    try:
        # start controller
        gpsc.start()



        while True:
            status = gpsc.fix.mode
            speed = (gpsc.fix.speed * 2.2369)



            #uc_north, uc_east, uc_head = (272772.43, 5194173.36, 207)
            #science_north, science_east, science_head = (272422.99, 5193611.66, 270)
            #dorn_north, dorn_east, dorn_head = (271683.60, 5192717.74, 270)
            #dornin_north, dornin_east, dornin_head = (271683.60, 5192717.74, 90)
            #lc_north, lc_east, lc_head = (271482.00, 5192322.00, 120)
            #lcg_north, lcg_east, lcg_head = (271558.00, 5192094.00, 15)
            #miller_north, miller_east, miller_head = (272146.66, 5193673.59, 0)
            #music_north, music_east, music_head = (272274.55, 5194166.35, 90)
            #down_north, down_east, down_head = (271802.00, 5195520.00, 200)
            #mc_north, mc_east, mc_head = (727723.42, 5192516.97, 5)
            #orange_north, orange_east, orange_head = (728391.34, 5194522.77, 275)
            #russell_north, russell_east, russell_head = (727207.93, 5195130.11, 180)
            #chestnut_north, chestnut_east, chestnut_head = (728413.82, 5194415.27, 85)

            if status <= 1:
                print "Searching for GPS Fix"
                #f.write('Searching for GPS\n')
                time.sleep(60)
            else:
                north, east, zone, band = utm.from_latlon(gpsc.fix.latitude, gpsc.fix.longitude)
                track = (north, east, gpsc.fix.latitude, gpsc.fix.longitude, gpsc.fix.track,
                         speed, gpsc.fix.epx, gpsc.fix.epy, gpsc.utc)

                # print track
                s = str(track)

                #tracker(stop_north, stop_east, stop_heading, circle_size, 'stop_name', 'mp3')

                #UC
                tracker(272772.43, 5194173.36, 207, 20, 'UC', 'uc')

                #science
                tracker(272422.99, 5193611.66, 270, 20,'Science', 'foo')

                #Dornblaser
                tracker(271683.60, 5192717.74, 270, 20, 'Dornblaser Out', 'dorn')

                # Dornblaser Inbound
                tracker(271683.60, 5192717.74, 90, 20, 'Dornblaser IN', 'dorn')

                #LC
                tracker(271482.00, 5192322.00, 120, 10, 'L&C', 'lc')

                #LC Gold
                tracker(271558.00, 5192094.00, 15, 20, 'L&C Gold', 'lcg')

                #Miller
                tracker(272146.6, 5193673.59,  0, 20, 'Miller Hall', 'miller')

                #Music
                tracker(272274.55, 5194166.35, 90, 20, 'Music', 'music')

                #Downtown Transfer
                tracker(271802.00, 5195520.00, 200, 20, 'Downtown Transfer', 'downtown')

                #Missoula College
                tracker(727723.42, 5192516.97, 5, 20, 'Missoula College', 'mc')

                # 5th and Orange
                tracker(728391.34, 5194522.77, 275, 20, '5th & Orange', '5th')

                #Russel and Dakota
                tracker(727207.93, 5195130.11, 180, 20, 'Russel & Dakota', 'russell')

                # 6th and Chestnut
                tracker(728413.82, 5194415.27, 85, 20, '6th & Chestnut', '6th')

                # Garage
                tracker(272933.21, 5194323.15, 250, 20, 'Garage', 'garage')

                #################################################################
                # PSA #

                gpsdate = datetime.datetime.strptime(gpsc.utc, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.timedelta(hours=7)

                date1 = datetime.datetime(2016, 3, 10, 7, 00)
                date2 = datetime.datetime(2016, 3, 10, 19, 00)

                if date1 <= gpsdate <= date2:
                    # Arthur and central
                    tracker(272119.36, 5192900.83, 0, 20, 'PSA', 'psa')
                else:
                    pass



            #f.flush()
            time.sleep(0.3)

    # Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    finally:
        print "Stopping gps controller"
        #f.close()
        gpsc.stopController()
        # wait for the tread to finish
        gpsc.join()

    print "Done"
