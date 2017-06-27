from cx_Freeze import setup, Executable
  
setup(
    name = "Torrent2httpServer",
    version = "0.2.7",
    description = "Downloads torrents and share it over HTTP",
    executables = [Executable("standalone/standalone.py")]
    )