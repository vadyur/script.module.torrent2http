from __future__ import absolute_import, with_statement

#import sys
import os
import xbmc, xbmcvfs, xbmcaddon
from .net import HTTP

__libbaseurl__ = "https://github.com/DiMartinoXBMC/script.module.torrent2http/raw/master/bin"
__settings__ = xbmcaddon.Addon(id='script.module.torrent2http')
__version__ = __settings__.getAddonInfo('version')
__plugin__ = __settings__.getAddonInfo('name') + " v." + __version__

def get_libname(platform):
    return ["torrent2http" + (".exe" if 'windows' in platform else "")]

def log(msg):
    try:
        xbmc.log("### [{}]: {}".format(__plugin__,msg,) )
    except UnicodeEncodeError:
        xbmc.log("### [{}]: {}".format(__plugin__,msg.encode("utf-8", "ignore"),) )
    except:
        xbmc.log("### [{}]: {}".format(__plugin__,'ERROR LOG',) )

def getSettingAsBool(setting):
    return __settings__.getSetting(setting).lower() == "true"

class LibraryManager():
    def __init__(self, dest_path, platform):
        self.dest_path = dest_path
        self.platform = platform

    def check_update(self):
        need_update=False
        if __settings__.getSetting('plugin_name')!=__plugin__:
            __settings__.setSetting('plugin_name', __plugin__)
            for libname in get_libname(self.platform):
                self.libpath = os.path.join(self.dest_path, libname)
                self.sizepath=os.path.join(self.dest_path, libname+'.size.txt')
                size=str(os.path.getsize(self.libpath))
                size_old=open( self.sizepath, "r" ).read()
                if size_old!=size:
                    need_update=True
        return need_update

    def update(self):
        if self.check_update():
            for libname in get_libname(self.platform):
                self.libpath = os.path.join(self.dest_path, libname)
                xbmcvfs.delete(self.libpath)
            self.download()

    def download(self):
        def failed(libname):
            text = 'Failed download {}!'.format(libname)
            xbmc.executebuiltin("XBMC.Notification({},{},{})".format(__plugin__,text,750))

        xbmcvfs.mkdirs(self.dest_path)
        for libname in get_libname(self.platform):
            dest = os.path.join(self.dest_path, libname)
            log("try to fetch {}".format(libname))
            url = "{}/{}/{}.zip".format(__libbaseurl__, self.platform, libname)
            try:
                import requests
                r = requests.get(url)
                if r.ok:
                    path_to_zip_file = dest + ".zip"
                    with open(path_to_zip_file, 'wb') as f:
                        f.write(r.content)
                        log("{} -> {}".format(url, dest))
                        import zipfile
                        with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
                            zip_ref.extractall(self.dest_path)
                        xbmcvfs.delete(path_to_zip_file)
                else:
                    failed(libname)
            except:
                failed(libname)
        return True
