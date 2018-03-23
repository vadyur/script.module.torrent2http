from ..engine import Engine
from ..error import Error
from ..remote.log import *
from .. import Encryption

from ..remote import filesystem

dht_routers 		= ["router.bittorrent.com:6881","router.utorrent.com:6881"]
user_agent 			= 'uTorrent/2200(24683)'

class LocalEngine(Engine):
	def LoadSettings(self):
		from ..remote.remotesettings import Settings
		self.settings = Settings()
		return self.settings

	def args2kwargs(self, *args, **kwargs):
		arg_names = ['uri', 'binaries_path', 'platform', 'download_path',
                 'bind_host', 'bind_port', 'connections_limit', 'download_kbps', 'upload_kbps',
                 'enable_dht', 'enable_lsd', 'enable_natpmp', 'enable_upnp', 'enable_scrape',
                 'log_stats', 'encryption', 'keep_complete', 'keep_incomplete',
                 'keep_files', 'log_files_progress', 'log_overall_progress', 'log_pieces_progress',
                 'listen_port', 'use_random_port', 'max_idle_timeout', 'no_sparse', 'resume_file',
                 'user_agent', 'startup_timeout', 'state_file', 'enable_utp', 'enable_tcp',
                 'debug_alerts', 'logger', 'torrent_connect_boost', 'connection_speed',
                 'peer_connect_timeout', 'request_timeout', 'min_reconnect_time', 'max_failcount',
                 'dht_routers', 'trackers', 'buffer']
			
		i = 0
		for arg in args:
			kwargs[arg_names[i]] = arg
			i += 1

		return kwargs

	def __init__(self, *args, **kwargs):
		try:
			s = self.LoadSettings()

			kwargs = self.args2kwargs(*args, **kwargs)
			args = []

			self.torrent_path = None
			uri = kwargs['uri']
			if uri.startswith('file:'):
				uri = uri.replace('file:', '')
				from urllib import url2pathname
				self.torrent_path = url2pathname(uri)
			elif uri.startswith('http:') or uri.startswith('https:'):
				# download torrent
				from urllib2 import urlopen
				h = urlopen(uri)
				self.torrent_path = 'tt.torrent'
				if filesystem.exists(self.torrent_path):
					filesystem.remove(self.torrent_path)

				with filesystem.fopen(self.torrent_path, 'wb') as t:
					from shutil import copyfileobj
					copyfileobj(h, t)

			if not self.torrent_path:
				self.settings.copy_torrent = False

			if s.use_global:
				''' Use global settings for all addons '''

				kwargs['encryption'] = Encryption.ENABLED if s.encryption else Encryption.DISABLED 
				kwargs['upload_kbps'] =  s.upload_limit * 1024
				kwargs['download_kbps'] =  s.download_limit * 1024

				if s.connections_limit:
					kwargs['connections_limit'] = s.connections_limit
				else:
					kwargs['connections_limit'] = None

				kwargs['use_random_port'] = s.use_random_port
				kwargs['listen_port'] = s.listen_port if s.listen_port else 6881

				if s.use_dht_routers:
					kwargs['dht_routers'] = dht_routers
					kwargs['enable_dht'] = True

				if s.change_user_agent:
					kwargs['user_agent'] = user_agent

		except BaseException as e:
			print_tb(e)

		finally:
			Engine.__init__(self, **kwargs)

	def GetTorrentStatus(self):
		f_status = self.file_status(self.file_id)
		status = self.status()
		
		if f_status is None or status is None:
			return None

		try:
			return { 	'downloaded' : 	int(f_status.download / 1024 / 1024),
						'size' : 		int(f_status.size / 1024 / 1024),
						'dl_speed' : 	int(status.download_rate),
						'ul_speed' :	int(status.upload_rate),
						'num_seeds' :	status.num_seeds, 
						'num_peers' :	status.num_peers
					}
		except:
			pass
			
		return None

	def get_playable_name(self):
		import os
		from afteractions import TorrentInfo
		info = TorrentInfo.get_torrent_info(self.torrent_path)

		try:
			if 'files' in info:
				for i, f in enumerate(info['files']):
					name = os.sep.join(f['path'])
					name = TorrentInfo.Name(info['name'])
					if i == int(self.file_id):
						return name
			else:
				return TorrentInfo.Name(info['name'])

		except UnicodeDecodeError:
			pass

		return None

	def close(self, closeEngine=True):
		try:
			settings = self.settings
			runner = None
			if settings.remove_files or settings.move_video or settings.copy_torrent:
				import afteractions
				runner = afteractions.Runner(settings, 
							self.get_playable_name(), 
							self.GetTorrentStatus(), 
							self.torrent_path)
		except BaseException as e:
			print_tb(e)
		finally:
			if closeEngine:
				Engine.close(self)

		try:
			if runner:
				runner.execute()
		except BaseException as e:
			print_tb(e)

	def start(self, start_index=None, startEngine=True):
		self.file_id = start_index

		if startEngine:
			Engine.start(self, start_index)