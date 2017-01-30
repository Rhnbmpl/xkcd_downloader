#!/usr/bin/python3
'''	XKCD_DOWNLOADER: Simple downloader to downloader all xkcd comics since the beginning of time and also automate 
	the downloading at your defined time(edit the cron entry section).Cheers!

MIT License

Copyright (c) 2017 Rohan Bampal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Please Raise any issues at: https://github.com/Rhnbmpl/xkcd_downloader/issues

'''

import os
import subprocess
import time
import datetime
end=''
start_url=''
path=''		# This contains the path of the Downlaod diretory('xkcd_multi')
cwd=os.path.dirname(os.path.realpath(__file__))		#get path to the directory where the program is in
tym=datetime.datetime.now().strftime('%H:%M:%S %d-%B-%Y')
print("---------LOG AT: %s --------"%(tym))		# all print statements and error recorded in prog.log file
if(os.path.exists('%s/dont_touch.config'%(cwd))==False):
	cwd=os.getcwd()		#This is the directory where the program is located, the config file will be made here
	conf=open('%s/dont_touch.config'%(cwd),'w')		#w=only write;r=only read;r+=read and write
	conf.close()
	end='#'
	print('\t\tMIT License\nCopyright (c) 2017 Rohan Bampal\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.')
	print('\n\n--- Please Raise any issues at: https://github.com/Rhnbmpl/xkcd_downloader/issues ---')
	print('Checking and installing required dependencies. Please enter password.......')
	try:
		subprocess.run('sudo pip3 install -r requirements.txt',shell=True)
	except:
		print("Error running pip3, make sure you have pip3 installed by: $ sudo apt-get install python3-pip")
		raise SystemExit
	print('Setting file xkcd_down_multi.py as executable.......')
	subprocess.run('sudo chmod a+x xkcd_down_multi.py',shell=True)
	print('---------------------------------------------------------------------------------------------')
	print('Setting up crontab entry for updating comics at 10am and 2 pm everyday.....')
	subprocess.run('crontab -l > mycron',shell=True)
	subprocess.run('echo "00 10,14 * * * %s/auto.py > %s/prog.log 2>&1 " >> mycron'%(cwd,cwd),shell=True)		#Diverting all outputs to a log file when run from cron. Easy looking for errors. prog.log stores the last run time and action taken
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
	print('Download in different directory?[y/n] If No, then it will be downlaoded in this directory')
	if(str(input()).lower()=='y'):
		print("Enter the full path of the directory to download the comics to")
		path=str(input())		#Download directory is in the same directory as the program
	else:
		path=cwd
	if(os.path.exists('%s/xkcd_multi'%(path))==False):
		os.makedirs('%s/xkcd_multi'%(path),exist_ok=True)
else:
	conf=open('%s/dont_touch.config'%(cwd),'r')
	line=(conf.readline()).split()
	# Config file format: "last_page_download_url last_image_url time date path_to_download_directory"		Seperated by space
	#                              ^line[0]        ^line[1] line[2]^   ^line[3]      ^line[4]  
	end=line[0]
	start_url=line[1]
	path=line[4]
	conf.close()


import xkcd_down_multi as downl
end,start_url=downl.main(end,start_url,path)

if(end=='nope'):
	print('----Already updated to latest----')

else:
	conf=open('%s/dont_touch.config'%(cwd),'w')#w=only write;r=only read;r+=read and write
	conf.write(end+' '+start_url+' '+tym+' '+path)
	conf.close()
	print("----Updated till: %s ----- \n----On Last run: %s -----"%(end,tym))
subprocess.run('rm %s/xkcd_multi/xkcd.txt'%(path),shell=True)
#print(cwd)




# crontab format: min hr date-of-mnth mnth day-of-wk [command]
