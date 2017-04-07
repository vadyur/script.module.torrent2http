import xbmcaddon, xbmc, filesystem

_bin_dir = xbmc.translatePath('special://home/addons/script.module.torrent2http/bin').decode('utf-8')
print _bin_dir.encode('utf-8')

_ADDON_NAME = 'script.module.torrent2http'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)


class Settings:
	def __init__(self, path=None):
		self.role           = _addon.getSetting("role").decode('utf-8')
		self.storage_path   = _addon.getSetting("storage_path").decode('utf-8')

		self.storage_path  = filesystem.abspath(self.storage_path)

		self.remote_host    = _addon.getSetting("remote_host").decode('utf-8')
		try:
			self.remote_port    = int(_addon.getSetting("remote_port"))
		except:
			self.remote_port = 28282

		self.binaries_path = _bin_dir


		self.use_global = bool(_addon.getSetting("remote_port") == 'true')

		self.upload_limit      = int(_addon.getSetting("upload_limit"))
		self.download_limit    = int(_addon.getSetting("download_limit"))
		self.encryption        = bool(_addon.getSetting("encryption") == 'true')
		self.connections_limit = int(_addon.getSetting("connections_limit"))
		self.listen_port       = int(_addon.getSetting("listen_port"))
		self.use_random_port   = bool(_addon.getSetting("use_random_port") == 'true')
		self.pre_buffer_bytes  = int(_addon.getSetting("pre_buffer_bytes"))

		xbmc.log(str(self.__dict__))

	def __getitem__(self, key):
		return self.__dict__[key]