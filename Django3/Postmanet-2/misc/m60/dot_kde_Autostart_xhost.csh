#!/bin/csh -f
/usr/bin/xhost +
/usr/bin/irxevent /etc/lircrc &
/usr/bin/irexec /etc/lircrc &

/usr/bin/ntfs-3g /dev/sda4 /mnt/dsh_lib -o uid=48 -o gid=48 -o force &

cp /dev/null /u/Postmanet/repository/WWW/logs/stderr.txt
cp /dev/null /u/Postmanet/repository/WWW/logs/stdout.txt

cd /dev
chmod -R a=u snd mixer dsp
cd /home/dmcuser

/usr/local/firefox/firefox &
