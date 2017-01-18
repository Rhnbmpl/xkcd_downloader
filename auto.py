#!/usr/bin/python3
'''	XKCD_DOWNLOADER: Simple downloader to downloader all xkcd comics since the beginning of time and also automate 
	the downloading at your defined time(edit the cron entry section).Cheers!

    Copyright (C) 2017  Rohan Bampal
    Contact me by mail at: rohanbampal@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program. It is located in the file 'LICENSES.txt'. If not, see <http://www.gnu.org/licenses/>.
'''

import os
import subprocess
import time
import datetime
end=''
start_url=''
cwd=os.path.dirname(os.path.realpath(__file__))#get path to the directory where the program is in
tym=datetime.datetime.now().strftime('%H:%M:%S %d-%B-%Y')
print("---------LOG AT: %s --------"%(tym))# all print statements and error recorded in prog.log file
if(os.path.exists('%s/dont_touch.config'%(cwd))==False):
	cwd=os.getcwd()
	conf=open('%s/dont_touch.config'%(cwd),'w')#w=only write;r=only read;r+=read and write
	conf.close()
	end='#'
	print('XKCD_DOWNLOADER  Copyright (C) 2017  Rohan Bampal \nThis program comes with ABSOLUTELY NO WARRANTY.\n This is free software, and you are welcome to redistribute it \nunder certain conditions\n')
	print('Checking and installing required dependencies. Please enter password.......')
	subprocess.run('sudo pip3 install -r requirements.txt',shell=True)
	print('Setting up crontab entry for updating comics at 10am and 2 pm everyday.....')
	subprocess.run('crontab -l > mycron',shell=True)
	subprocess.run('echo "00 10,14 * * * %s/auto.py > %s/prog.log 2>&1 " >> mycron'%(cwd,cwd),shell=True)#Diverting all outputs to a log file when run from cron. Easy looking for errors. prog.log stores the last run time and action taken
	subprocess.run('crontab mycron',shell=True)
	subprocess.run('rm mycron',shell=True)
	print('Do you want to update comics on startup?[y/n]')
	if(str(input()).lower()=='y'):
		subprocess.run('crontab -l > mycron',shell=True)
		subprocess.run('echo "@reboot %s/auto.py > %s/prog.log 2>&1 " >> mycron'%(cwd,cwd),shell=True)
		subprocess.run('crontab mycron',shell=True)
		subprocess.run('rm mycron',shell=True)
	else:
		pass
else:
	conf=open('%s/dont_touch.config'%(cwd),'r')
	line=(conf.readline()).split()
	end=line[0]
	start_url=line[1]
	conf.close()

if(os.path.exists('xkcd_multi')==False):
	os.makedirs('xkcd_multi',exist_ok=True)

import xkcd_down_multi as downl
end,start_url=downl.main(end,start_url)
if(end=='nope'):
	print("----Already updated to latest-----")

else:
	conf=open('%s/dont_touch.config'%(cwd),'w')#w=only write;r=only read;r+=read and write
	conf.write(end+' '+start_url+' '+tym)
	conf.close()
	print("----Updated till: %s ----- On Last run: %s -----"%(end,tym))
subprocess.run('rm %s/xkcd.txt'%(cwd),shell=True)
#print(cwd)




# crontab format: min hr date-of-mnth mnth day-of-wk [command]
