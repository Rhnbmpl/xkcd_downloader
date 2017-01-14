#!/usr/bin/python3
import webbrowser as web
import requests
import bs4
import os
import sys
import threading
import time
import subprocess
def down(down_url,prev_addr,cwd):
	try:
			res=requests.get('http:'+down_url)
			print('Downloading Image......%s'%('http:'+down_url))
			imgfile=open('%s/xkcd_multi/'%(cwd)+os.path.basename(down_url),'wb')
			for chunk in res.iter_content(100000):	#write in chunks of 100000 to prevent memory leaks
				imgfile.write(chunk)
			imgfile.close()
	except:
			print('Error downloading image : %s'%(prev_addr))
			pass
def main(end,start_url):
	cwd=os.path.dirname(os.path.realpath(__file__))#get path to the directory where the program is in
	fst=0
	ret=['','']
	downthr_lst=[]
	addr='http://www.xkcd.com'
	#end=list(sys.argv)
	prev_addr=addr
	prev_url=''
	error=[]
	while True:
		s=requests.Session()
		pg=s.get(prev_addr)
		try:
			pg.raise_for_status()
		except Exception as exc:
			if(pg.status_code==504):
				print('Error fetching page: %s'%(exc))
				print('Skipping comic : %s'%(prev_addr))
				error.append(prev_addr)
				prev_url=int(prev_url.replace('/',''))
				prev_url=prev_url-1
				prev_url=str(prev_url)
				prev_url='/'+prev_url+'/'
				prev_addr=addr+prev_url
				continue
			else:
				print('Error feteching page : %s'%(exc))
				error.append(prev_addr)
		file=open('%s/xkcd.txt'%(cwd),'wb')
		for chunk in pg.iter_content(100000):
			file.write(chunk)
		soup=bs4.BeautifulSoup(pg.text,'lxml')
		img=soup.select('#comic img')
		if img==[]:
			print('--------Could not find image : %s-------'%(prev_addr))
			error.append(prev_addr)
		else:
			down_url=img[0].get('src')

			if(down_url==start_url and fst==0):
				print(start_url+" ....Exists, no new comics :'( ....")
				ret=['nope','nope']
				return ret
			elif(fst==0):
				ret[1]=down_url
			else:
				pass

			down_thr=threading.Thread(target=down,args=(down_url,prev_addr,cwd))
			downthr_lst.append(down_thr)
			down_thr.start()
			
		file.close()
		prev=soup.select('a[rel="prev"]')
		prev_url=prev[0].get('href')
		if(fst==0):
			start=prev_url
			start=int(start.replace('/',''))
			start=str(start+1)
			ret[0]='/'+start+'/'
			fst=1

		if (prev_url==end):
			break
		else:
			prev_addr=addr+prev_url
	for down_thr in downthr_lst:
		down_thr.join()
	print('-----------Errors: %d -----------'%(len(error)))
	for k in range(0,len(error)):
		print(error[k])
	print('--------------Done--------------')
	return ret