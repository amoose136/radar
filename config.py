__author__ ='Amos Manneschmidt'
import urllib, sys
from workflow import Workflow
ws = sys.argv[1]

def main(wf):	
	from PIL import Image	

	urllib.urlretrieve("http://radar.weather.gov/Overlays/Topo/Short/" + ws + "_Topo_Short.jpg",'static/r.gif') #topographical map
	urllib.urlretrieve("http://radar.weather.gov/Overlays/County/Short/" + ws + "_County_Short.gif",'static/1.gif') #Counties map
	urllib.urlretrieve("http://radar.weather.gov/Overlays/Highways/Short/" + ws + "_Highways_Short.gif",'static/2.gif') #Highways map
	urllib.urlretrieve("http://radar.weather.gov/Overlays/Cities/Short/" + ws + "_City_Short.gif",'static/3.gif')	#Cities labels map
	print(ws)


	overlay=Image.open('static/1.gif').convert('RGBA')
	a=Image.open('static/2.gif').convert('RGBA')
	b=Image.open('static/3.gif').convert('RGBA')
	overlay.paste(a,(0,0),a)
	overlay.paste(b,(0,0),b)
	info=overlay.info
	info['transparency']=0
	overlay.save('static/overlay.gif',**info)

	grayscale = Image.open('static/r.gif').convert('L')
	grayscale = grayscale.point(lambda p: p * 0.25)
	grayscale.save('static/grayscale.gif')

if __name__ == '__main__':
	wf = Workflow(libraries=['./lib'])
	sys.exit(wf.run(main))
