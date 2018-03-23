# -*- coding: utf-8 -*-

from ..remote.log import debug, print_tb


import os
import urllib

from ..remote import filesystem

class TorrentInfo:
	@staticmethod
	def is_playable(name):
		filename, file_extension = os.path.splitext(name)
		return file_extension in ['.mkv', '.mp4', '.ts', '.avi', '.m2ts', '.mov']

	@staticmethod
	def get_torrent_info(torrent_path):
		data = None
		with filesystem.fopen(torrent_path, 'rb') as torr:
			data = torr.read()

		if data is None:
			return None

		from bencode import BTFailure
		try:
			from bencode import bdecode
			decoded = bdecode(data)
		except BTFailure:
			debug("Can't decode torrent data (invalid torrent link?)")
			return None

		return decoded['info']


	@staticmethod
	def Name(name):
		try:
			return name.decode('utf-8')
		except UnicodeDecodeError:
			import chardet
			enc = chardet.detect(name)
			if enc['confidence'] > 0.7:
				try:
					name = name.decode(enc['encoding'])
				except UnicodeDecodeError:
					pass
				return name
			else:
				log.print_tb()

	def __init__(self, path):
		self.torrent_path = path

	def GetTorrentData(self):
		info = TorrentInfo.get_torrent_info(self.torrent_path)

		import hashlib
		from bencode import bencode
		self.info_hash = hashlib.sha1(bencode(info)).hexdigest()
		#debug(self.info_hash)

		name = '.'
		playable_items = []
		try:
			if 'files' in info:
				for i, f in enumerate(info['files']):
					# debug(i)
					# debug(f)
					name = os.sep.join(f['path'])
					size = f['length']
					#debug(name)
					if TorrentInfo.is_playable(name):
						playable_items.append({'index': i, 'name': TorrentInfo.Name(name), 'size': size})
					name = TorrentInfo.Name(info['name'])
			else:
				playable_items = [ {'index': 0, 'name': TorrentInfo.Name(info['name']), 'size': info['length'] } ]
		except UnicodeDecodeError:
			return None

		return { 'info_hash': self.info_hash, 'files': playable_items, 'name': name }


class Runner(object):
	def __init__(self, settings, playable_name, torrent_status, torrent_path):
		#self.command = settings.script_params.split(u' ')
		self.settings = settings
		self.torrent_status = torrent_status
		self.torrent_path = torrent_path
		self.playable_name = playable_name

		self.torrent_data = TorrentInfo(torrent_path).GetTorrentData()

		debug('-' * 30 + ' Runner ' + '-' * 30)
		debug('torrent: ' + self.torrent)
		debug('videofile: ' + self.videofile)
		debug('relativevideofile: ' + self.relativevideofile)
		#debug('torrent_source: ' + self.torrent_source)
		#debug('short_name: ' + self.short_name)
		debug('downloaded: ' + str(self.downloaded))
		#debug('videotype: ' + self.videotype)

	def execute(self):
		"""
		if settings.run_script:
			self.process_params()
			self.run()
		"""
		settings = self.settings

		if settings.remove_files:
			debug('Runner: remove_files')
			if filesystem.exists(self.videofile):
				filesystem.remove(self.videofile)

		if float(self.downloaded) > 99 and self.all_torrent_files_exists():

			if settings.move_video and settings.copy_video_path and filesystem.exists(settings.copy_video_path):
				self.move_video_files()

			if settings.copy_torrent and settings.copy_torrent_path and filesystem.exists(settings.copy_torrent_path):
				self.copy_torrent()		

	def copy_torrent(self):
		debug('Runner: copy torrent')
		dest_path = filesystem.join(self.settings.copy_torrent_path, filesystem.basename(self.torrent_path))
		filesystem.copyfile(self.torrent_path, dest_path)

	def move_video_files(self):
		debug('Runner: move video')
		for file in self.get_relative_torrent_files_list():
			dest_path = filesystem.join(self.settings.copy_video_path, file)

			if not filesystem.exists(filesystem.dirname(dest_path)):
				filesystem.makedirs(filesystem.dirname(dest_path))

			src_path = filesystem.join(self.storage_path, file)
			if not filesystem.exists(src_path):
				continue

			if not filesystem.exists(dest_path):
				# Move file if no exists
				filesystem.movefile(src_path, dest_path)
			else:
				filesystem.remove(src_path)

	def all_torrent_files_exists(self):
		files = self.torrent_data['files']
		data = self.torrent_data

		for item in files:
			path = filesystem.join(self.storage_path, data['name'], item['name'])
			debug(u'all_torrent_files_exists: ' + path)
			if not filesystem.exists(path):
				path = filesystem.join(self.settings.copy_video_path, data['name'], item['name'])
				debug(u'all_torrent_files_exists: ' + path)
				if not filesystem.exists(path):
					debug(u'all_torrent_files_exists: not found')
					return False

		debug(u'all_torrent_files_exists: Ok')
		return True


	def get_relative_torrent_files_list(self):
		files = self.torrent_data['files']
		return [filesystem.join(self.torrent_data['name'], item['name']) for item in files]

	@property
	def torrent(self):
		return self.torrent_path

	@property
	def storage_path(self):
		result = self.settings.storage_path
		if result == '':
			import xbmc
			result = xbmc.translatePath('special://temp').decode('utf-8')
		return result


	@property
	def videofile(self):
		return filesystem.join(self.storage_path, self.relativevideofile)

	@property
	def relativevideofile(self):
		with filesystem.fopen(self.torrent_path, 'rb') as torr:
			data = torr.read()

			if data is None:
				return self.playable_name

			from bencode import BTFailure
			try:
				from bencode import bdecode
				decoded = bdecode(data)
			except BTFailure:
				debug("Can't decode torrent data (invalid torrent link?)")
				return self.playable_name

			info = TorrentInfo.get_torrent_info(self.torrent_path)

			if 'files' in info:
				return filesystem.join(TorrentInfo.Name(info['name']), self.playable_name)

		return self.playable_name

	@property
	def downloaded(self):
		status = self.torrent_status
		if status is None:
			return 0

		try:
			return str(round(status['downloaded'] * 100 / status['size']))
		except BaseException as e:
			print_tb(e)
			return 0

	"""
	def process_params(self):
		for i, s in enumerate(self.command):
			if '%t' in s:
				self.command[i] = s.replace('%t', self.torrent)
			if '%f' in s:
				self.command[i] = s.replace('%f', self.videofile)
			if '%F' in s:
				self.command[i] = s.replace('%F', self.relativevideofile)
			if '%u' in s:
				self.command[i] = s.replace('%u', self.torrent_source)
			if '%s' in s:
				self.command[i] = s.replace('%s', self.short_name)
			if '%p' in s:
				self.command[i] = s.replace('%p', self.downloaded)
			if '%v' in s:
				self.command[i] = s.replace('%v', self.videotype)

			self.command[i] = self.command[i].encode('utf-8')

	def run(self):
		debug(self.command)
		import subprocess

		startupinfo = None
		u8runner = None

		if os.name == 'nt':
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= 1
			startupinfo.wShowWindow = 0
			u8runner = filesystem.abspath(filesystem.join(Runner.get_addon_path(), 'bin/u8runner.exe')).encode('mbcs')

		shell = self.command[0].startswith('@')
		if shell:
			self.command[0] = self.command[0][1:]

		try:
			subprocess.call(executable=u8runner, args=self.command, startupinfo=startupinfo, shell=shell)
		except OSError, e:
			debug(("Can't start %s: %r" % (str(self.command), e)))
		except BaseException as e:
			print_tb(e)
	"""

class TestRunner(Runner):
	def __init__(self):
		pass


def test_resume(tr):
	dest = u'/mnt/videocache/фываолдж'
	Runner.change_resume_file(tr, dest)


def test_get_relative_torrent_files_list(tr):
	l = Runner.get_relative_torrent_files_list(tr)
	for f in l:
		print f


if __name__ == '__main__':
	tr = TestRunner()
	tr.resume_file = r'c:\Bin\626bbfbb61755200069486609d66e53146483ebe.resume'
	tr.torrent_path = r'c:\Users\vd\AppData\Roaming\Kodi\userdata\addon_data\script.media.aggregator\nnmclub\507983.torrent'

	test_resume(tr)

	#test_get_relative_torrent_files_list(tr)