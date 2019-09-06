# Version 3
import urllib2
import time
#import git

flag_internet = False

# has internets
def internet_on():
    try:
        response=urllib2.urlopen('http://google.com',timeout=5)
        print 'internet'
        return True
    except urllib2.URLError as err: pass
    return False

# sync

def sync():
    global flag_internet
    if internet_on():
        time.sleep(3)
        while not flag_internet:
            print 'start update'
            #os.system('/home/pi/Desktop/GPS/sync.sh')
            #log.write('\n Ran sync script')
            flag_internet = True
    else:
        return




if __name__ == '__main__':
    try:

        while internet_on():
            sync()
            time.sleep(2)
            break
        else:
            print 'Waiting'
            time.sleep(2)

    # Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    finally:
        print "Stopping gps controller"


    print "Done"
