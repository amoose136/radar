import sys, os, argparse, plistlib as pl
from subprocess import call
from workflow import Workflow, ICON_INFO
from workflow.background import run_in_background, is_running
from plistlib import readPlist

__version=pl.readPlist('info.plist')['version']
UPDATE_SETTINGS = {'github_slug':'amoose136/radar','version':__version}
HELP_URL = 'https://github.com/amoose136/radar/issues'

log = None
def main(wf):
	if wf.update_available:
		wf.add_item('New version available','Action this item to install the update',autocomplete=':update',valid=False)
	
	log.debug('Main Started')
	# build argument parser to parse script args and collect their
	parser = argparse.ArgumentParser()
	# add an optional query and save it to 'query'
	parser.add_argument('text', nargs='?', default=None)
	# parse the script's arguments
	args = parser.parse_args(wf.args)

	try:
		ws = pl.readPlist('info.plist')['variables']['ws']
	except:
		ws = ''
		wf.add_item('Error with env vars','Please report to developer (tab) or try reconfiguring',autocomplete=':help',valid=False)
	if os.path.isfile('static/overlay.gif') and os.path.isfile('static/grayscale.gif') and ws!= '':
		if  wf.args[0]=='':
			wf.add_item('Radar','Download latest NOAA radar images',arg=ws,valid=True)
		if len(wf.args[0])<2:
			wf.add_item('Radar [Location]','Find local station, cache local static data',autocomplete=' ',valid=False)
	else:
		wf.add_item('Radar','Must (re)congfigure location first: autocomplete this item and type your location',autocomplete=' ',valid=False)
	
	wf.send_feedback()

def help():
	wf.open_help()

if __name__ == '__main__':
	wf = Workflow(libraries=['./lib'], 
				update_settings=UPDATE_SETTINGS,
				help_url=HELP_URL,
				capture_args=True)
	log=wf.logger
	wf.magic_prefix=':'
	sys.exit(wf.run(main))