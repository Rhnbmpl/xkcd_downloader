# xkcd_downloader
Download all xkcd comics(since the beginning of time) from http://www.xkcd.com. Downloading done by multhreading in Python.
Download starts from the latest comic to the oldest one.
No limit on number of threads used. Will try to use maximum bandwidth. Images having problems to download is shown in the
end when all others have finished donloading.

extra modules needed: requests , bs4
Intstallation: sudo pip3 install (module_name)

-----------EDIT--------------

Added auto.py which automates the downloading of the comics with putting entries in crontab, update timings can be modified.
auto.py has to be made executable and be owned by root in order for it to be added to cronjobs.

$sudo chmod a+x auto.py
$sudo chmod a+x xkcd_down_multi.py
$./auto.py

Thats it. Directory 'xkcd_multi' will be created where the comics will be stored(same directory as the 'auto.py' and
'xkcd_multi_down.py'. To view lastest, order by date modified.
'config.log' will be created in which 'auto.py'(running from cron) outputs to see when the 'auto.py' ran from the cron and 
if it encountered any errors.
