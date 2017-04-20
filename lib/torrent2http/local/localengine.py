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

	def __init__(self, **kwargs):
		s = self.LoadSettings()

		uri = kwargs['uri']
		if uri.startswith('file:'):
			uri = uri.replace('file:', '')
			from urllib import url2pathname
			self.torrent_path = url2pathname(uri)

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

			if s.change_user_agent:
				kwargs['user_agent'] = user_agent
		
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
		settings = self.settings
		runner = None
		if settings.remove_files or settings.move_video or settings.copy_torrent:
			import afteractions
			runner = afteractions.Runner(settings, 
						self.get_playable_name(), 
						self.GetTorrentStatus(), 
						self.torrent_path)

		if closeEngine:
			Engine.close(self)

		if runner:
			runner.execute()

	def start(self, start_index=None, startEngine=True):
		self.file_id = start_index

		if startEngine:
			Engine.start(self, start_index)