#!/bin/sh

THISHOST=$(hostname -f)
echo $THISHOST
# Daily Data Backup
rsync -rvP -e 'ssh -p 666' --remove-sent-files /home/pi/Desktop/GPS/logs busdump@spacefighter.noip.me:~/busdumps/$THISHOST


#sync from server
rsync -u -rvP -e 'ssh -p 666' busdump@spacefighter.noip.me:~/busdumps/GPS/ /home/pi/Desktop/GPS/

# play file so I know it works
mpg321 -q /home/pi/Desktop/GPS/audio/update.mp3