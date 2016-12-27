#!/usr/bin/python3
import os
import subprocess,time,datetime
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
	print('Setting up crontab entry for updating comics at 10am and 2 pm everyday.....')
	subprocess.run('crontab -l > mycron',shell=True)
	subprocess.run('echo "00 10,14 * * * %s/auto.py > %s/prog.log 2>&1 " >> mycron'%(cwd,cwd),shell=True)#Diverting all outputs to a log file when run from cron
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