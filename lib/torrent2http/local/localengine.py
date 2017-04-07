from ..engine import Engine
from ..error import Error
from ..remote.log import *

class LocalEngine(Engine):
	def __init__(self, **kwargs):
		from ..remote.remotesettings import Settings
		s = Settings()

		if s.use_global:
			''' Use global settings for all addons '''

			kwargs['encryption'] = Encryption.ENABLED if s.encryption else Encryption.DISABLED 
			kwargs['upload_limit'] =  s.upload_limit * 1024
			kwargs['download_limit'] =  s.download_limit * 1024

			if s.connections_limit:
				kwargs['connections_limit'] = s.connections_limit
			else:
				kwargs['connections_limit'] = None

			kwargs['use_random_port'] = s.use_random_port
			kwargs['listen_port'] = s.listen_port if s.listen_port else 6881
		

		Engine.__init__(self, **kwargs)
