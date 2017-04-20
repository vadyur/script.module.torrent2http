import xbmcaddon, xbmc, filesystem

_bin_dir = xbmc.translatePath('special://home/addons/script.module.torrent2http/bin').decode('utf-8')
print _bin_dir.encode('utf-8')

_ADDON_NAME = 'script.module.torrent2http'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)

def get_bool(s, default=False):
	try:
		return _addon.getSetting(s) == 'true'
	except:
		return default

def get_int(s, default=0):
	try:
		return int(_addon.getSetting(s))
	except:
		return default

def get_unicode(s, default=u""):
	try:
		return _addon.getSetting(s).decode('utf-8')
	except:
		return default


class Settings:

	def __init__(self, path=None):
		self.role           = get_unicode("role")

		self.storage_path  = filesystem.abspath(get_unicode("storage_path"))
		self.remote_host    = get_unicode("remote_host")
		self.remote_port    = get_int("remote_port", 2829)

		self.binaries_path = _bin_dir

		self.use_global		= get_bool("use_global")

		self.upload_limit      = get_int("upload_limit")
		self.download_limit    = get_int("download_limit")
		self.encryption        = get_bool("encryption")
		self.connections_limit = get_int("connections_limit")
		self.listen_port       = get_int("listen_port")
		self.use_random_port   = get_bool("use_random_port")
		self.pre_buffer_bytes  = get_int("pre_buffer_bytes")

		self.use_dht_routers	= get_bool("use_dht_routers")
		self.change_user_agent	= get_bool("change_user_agent")

		self.move_video         = get_unicode("action_files") == u'переместить'
		self.remove_files       = get_unicode("action_files") == u'удалить'

		self.copy_video_path	= get_unicode("copy_video_path")
		self.copy_torrent		= get_bool("copy_torrent")
		self.copy_torrent_path	= get_unicode("copy_torrent_path")

		xbmc.log(str(self.__dict__))

	def __getitem__(self, key):
		return self.__dict__[key]