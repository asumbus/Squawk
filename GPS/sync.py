# Version 3

from gps import *
import os
import time
import threading
import utm
import datetime
import urllib2


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

#######################################################

# set Flags all off to start with.

flag_internet = False
flag_log = False


# set to something to start with.
s = 1
track = 1


# has internets

def internet_on():
    try:
        response=urllib2.urlopen('http://google.com',timeout=5)
        return True
    except urllib2.URLError as err: pass
    return False

# sync

def sync():
    global flag_internet
    if internet_on():
        time.sleep(30)
        while not flag_internet:
            os.system('/home/pi/Desktop/GPS/sync.sh')
            #log.write('\n Ran sync script')
            flag_internet = True
    else:
        return


def startlog():
    global flag_log, logdate, log, status
    while not flag_log:
        log = open('/home/pi/Desktop/GPS/logs/' + logdate + '.txt', 'w')
        flag_log = True
        return log



if __name__ == '__main__':
    # create the controller
    gpsc = GpsController()
    try:
        # start controller
        gpsc.start()


        while True:

            sync()

            status = gpsc.fix.mode
            speed = (gpsc.fix.speed * 2.2369)

            if status <= 1:
                print "Searching for GPS Fix"
                time.sleep(2)
            else:

                north, east, zone, band = utm.from_latlon(gpsc.fix.latitude, gpsc.fix.longitude)
                track = north, east, gpsc.fix.latitude, gpsc.fix.longitude, gpsc.fix.track, \
                        speed, gpsc.fix.epx, gpsc.fix.epy, gpsc.utc

                gpsdate = datetime.datetime.strptime(gpsc.utc, '%Y-%m-%dT%H:%M:%S.%fZ') - datetime.timedelta(hours=6)
                logdate = str(gpsdate)
                # print track
                startlog()
                s = str(track)



                #print '\n', s, '', gpsdate

                log.write('\n' + s + ',' + logdate)


                log.flush()








            time.sleep(2)

    # Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    finally:
        print "Stopping gps controller"
        gpsc.stopController()
        # wait for the tread to finish
        gpsc.join()

    print "Done"
