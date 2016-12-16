#!/usr/bin/python3
import webbrowser as web
import requests,bs4,os,sys,threading,time
addr='http://www.xkcd.com'
#end=list(sys.argv)
prev_addr=addr
prev_url=''
error=[]
end='#'
if(os.path.exists('xkcd_multi')==False):
	os.makedirs('xkcd_multi',exist_ok=True)
def down(down_url,prev_addr):
	try:
			res=requests.get('http:'+down_url)
			print('Downloading Image......%s'%('http:'+down_url))
			imgfile=open('xkcd_multi/'+os.path.basename(down_url),'wb')
			for chunk in res.iter_content(100000):	#write in chunks of 100000 to prevent memory leaks
				imgfile.write(chunk)
			imgfile.close()
	except:
			print('Error downloading image : %s'%(prev_addr))
			pass
downthr_lst=[]
while 1:
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
	file=open('xkcd.txt','wb')
	for chunk in pg.iter_content(100000):
		file.write(chunk)
	soup=bs4.BeautifulSoup(pg.text,'lxml')
	img=soup.select('#comic img')
	if img==[]:
		print('--------Could not find image : %s-------'%(prev_addr))
		error.append(prev_addr)
	else:
		down_url=img[0].get('src')
		down_thr=threading.Thread(target=down,args=(down_url,prev_addr))
		downthr_lst.append(down_thr)
		down_thr.start()
		
	file.close()
	prev=soup.select('a[rel="prev"]')
	prev_url=prev[0].get('href')
	if (prev_url==end):
		break
	else:
		prev_addr=addr+prev_url
for down_thr in downthr_lst:
	down_thr.join()
print('-----------Errors-----------')
for k in range(0,len(error)):
	print(error[k])
print('------------Done------------')