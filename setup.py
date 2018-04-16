from cx_Freeze import setup, Executable
  
setup(
    name = "Torrent2httpServer",
    version = "0.3.1",
    description = "Downloads torrents and share it over HTTP",
    executables = [Executable("standalone/standalone.py")]
    )