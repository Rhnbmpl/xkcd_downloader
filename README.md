# xkcd_downloader
Download all xkcd comics(since the beginning of time) from http://www.xkcd.com. Downloading done by multhreading in Python.
Download starts from the latest comic to the oldest one.
No limit on number of threads used. Will try to use maximum bandwidth. Images having problems to download is shown in the
end when all others have finished donloading.

extra modules needed(will be downloaded automatically on first run if you have pip3 or pip): requests , bs4

Required dependancies(above mentioned modules) will be checked and downloaded by auto.py on first run.

Added auto.py which automates the downloading of the comics with putting entries in crontab, update timings can be modified.
auto.py has to be made executable and be owned by root in order for it to be added to cronjobs.

```
$ sudo chmod a+x auto.py
$ ./auto.py
```

Thats it. 

Directory 'Download_xkcd' will be created where the comics will be stored(same directory as the 'auto.py' and
'xkcd_multi_down.py' by default unless prompted on the first run, you can enter the directory where the download 
directory will be made and all comics will be downloaded there.All information regarding previous download url,time,
date,download directory path is recorded in 'dont_touch.config' file which is important for automatic download.

**Config file format: "*\<last_page_download_url> \<last_image_url> \<time> \<date> \<path_to_download_directory>*"** They are space seperated.

To view the lastest downloaded comics, order by date modified.
'config.log' will be created in which 'auto.py'(running from cron) outputs to see when the 'auto.py' ran from the cron and 
if it encountered any errors.
