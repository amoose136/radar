# Noaa weather radar downloader
#import needed things
__author__ ='Amos Manneschmidt'

from workflow import Workflow
import sys, os, urllib, signal, time
import subprocess as sp
from subprocess import Popen

loc=sys.argv[1] # set weather station code to query from alfred
anmdir = "animations/"
staticdir = "static/"
#Also do some BS to make libaries work in remote installations
def main(wf):
	import numpy, imageio
	from PIL import Image
	from bs4 import BeautifulSoup as BS

	#####################################################
	#setup initial "quick" static image
	print("Getting images...")
	urllib.urlretrieve("http://radar.weather.gov/Warnings/Short/"+loc+"_Warnings_0.gif","static/wn.gif") #warnings layer
	urllib.urlretrieve("http://radar.weather.gov/Legend/N0R/"+loc+"_N0R_Legend_0.gif","static/lg.gif") #legends
	urllib.urlretrieve("http://radar.weather.gov/RadarImg/N0R/"+loc+"_N0R_0.gif","static/rd.gif") #static radar

	bg=Image.open(staticdir+"grayscale.gif").convert('RGBA')	#bg=background image
	cnty=Image.open(staticdir+"overlay.gif").convert('RGBA')	#cnty=county, roads, state, city overlay
	wn=Image.open(staticdir+"wn.gif").convert('RGBA')# wn=warnings layer
	cnty.paste(wn,(0,0),wn)
	rd=Image.open(staticdir+"rd.gif").convert('RGBA')
	lg=Image.open(staticdir+"lg.gif").convert('RGBA')
	temp=Image.open(staticdir+"grayscale.gif").convert('RGBA')
	temp.paste(rd,(0,0),rd)
	temp.paste(cnty,(0,0),cnty)
	temp.paste(lg,(0,0),lg)
	temp.save(staticdir+'radar static.gif')

	#open saved static image with quicklook silencing output
	null = open(os.devnull,'wb')
	p=sp.Popen(['qlmanage', '-p', staticdir+'radar static.gif'],stderr=null,stdout=null)

	######################################################################
	#Parse html for links and download the 6 most recent images for region
	html = urllib.urlopen("http://radar.weather.gov/RadarImg/N0R/"+loc+"/?C=M;O=D")
	soup = BS(html,"html.parser")

	names=['']*6
	for i in range(5,11):
		n=i-5
		names[n]=soup.find_all('a')[i]['href'][:-4]
		print("downloading image "+names[n]+".gif")
		urllib.urlretrieve("http://radar.weather.gov/RadarImg/N0R/"+loc+"/"+names[n]+".gif",anmdir+names[n]+".gif")
		urllib.urlretrieve("http://radar.weather.gov/Legend/N0R/"+loc+"/"+names[n]+"_Legend.gif",anmdir+names[n]+"_Legend.gif")
		print("     downloaded image "+names[n]+".gif")

	print("   done")

	########################################################
	#Composite together overlay and underlay for each images
	print("Compositing..")
	images=['']*6
	for i,n in enumerate(names):
	 	im=Image.open(anmdir+n+".gif").convert('RGBA')
	 	lg=Image.open(anmdir+n+"_Legend.gif").convert('RGBA')
	 	temp=Image.open(staticdir+"grayscale.gif").convert('RGBA')
	 	temp.paste(im,(0,0),im)
	 	temp.paste(cnty,(0,0),cnty)
	 	temp.paste(lg,(0,0),lg)
	 	temp.save(anmdir+n+".gif")
	 	images[5-i]=imageio.imread(anmdir+n+".gif")
	print("   done")

	print("Saving/Compiling...")
	imageio.mimwrite("radar.gif",images,duration=[.25,.25,.25,.25,.25,1.5])
	print("   done")
	if not p.poll() and p.poll() != 0:
		print("Displaying...")
		np=sp.Popen(['qlmanage', '-p', 'radar.gif'],stderr=null,stdout=null)
		
		time.sleep(1)
		p.kill()
		sp.Popen("rm animations/*",shell=True)
		print("   done")
	print("Alfred Script done")

if __name__ == '__main__':
	wf = Workflow(libraries=['./lib'])
	sys.exit(wf.run(main))


