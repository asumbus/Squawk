# Version 3
import urllib2
import time
import subprocess


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
            output = subprocess.check_output(["git", "pull"])
            output
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
        print "Closing out of update"


    print "Done"
