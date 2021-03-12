import xbmcaddon, xbmc

from .filesystem import ensure_unicode, abspath

_bin_dir = ensure_unicode(xbmc.translatePath('special://home/addons/script.module.torrent2http/bin'))
print (_bin_dir)

_ADDON_NAME = 'script.module.torrent2http'
_addon = xbmcaddon.Addon(id=_ADDON_NAME)


class Settings:
	def __init__(self, path=None):
		self.role           = ensure_unicode(_addon.getSetting("role"))
		self.storage_path   = ensure_unicode(_addon.getSetting("storage_path"))

		self.storage_path  = abspath(self.storage_path)

		self.remote_host    = ensure_unicode(_addon.getSetting("remote_host"))
		try:
			self.remote_port    = int(_addon.getSetting("remote_port"))
		except:
			self.remote_port = 28282

		self.binaries_path = _bin_dir

		xbmc.log(str(self.__dict__))