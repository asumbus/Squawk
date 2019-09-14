# Version 3
import urllib2
import time
import subprocess


flag_internet = False
count = 0

# has internets
def internet_on():
    try:
        response=urllib2.urlopen('http://google.com',timeout=5)
        print 'found the internets'
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
            output = subprocess.check_output(["git", "pull"], cwd='home/pi/Desktop')
            output
            flag_internet = True
    else:
        return




if __name__ == '__main__':
    try:
        while True:
            print count
            if internet_on():
                sync()
                time.sleep(10)
                break
            elif count >= 10:
                print 'Cant live without internets!'
                break
            else:
                print 'Waiting for internets'
                count += 1
                time.sleep(60)

    # Ctrl C
    except KeyboardInterrupt:
        print "User cancelled"

    finally:
        print "Closing out of update"


    print "Done"
