# -*- coding: utf-8 -*-
from __future__ import absolute_import

import xbmc, sys

from torrent2http.remote.server import Server
from torrent2http.remote.log import debug

def main():
	debug('Starting server')
	
	server = Server()
	server.loop()
	monitor = xbmc.Monitor()
	
	try:
		while not monitor.abortRequested():
			if monitor.waitForAbort(1):
				break
			server.loop()
			xbmc.sleep(10)
			
	except KeyboardInterrupt:
		# Exit on ctrl+C
		debug('Exit')
		server.stop()
		sys.exit()
		
	debug('Exit')
	server.stop()

if __name__ == '__main__':
	from .torrent2http.remote.remotesettings import Settings
	s = Settings(None)

	if s.role == 'server':
		main()
