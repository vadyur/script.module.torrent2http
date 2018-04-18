import sys, os

if getattr(sys, 'frozen', False):
	# frozen
	print "frozen"
	#current = sys._MEIPASS
	current = os.path.dirname(sys.executable)
	print current
	print os.getcwd()
	
	sys.path.insert(0, os.path.normpath(os.path.join(current, 'standalone')))
else:
	# unfrozen
	current = os.path.dirname(os.path.realpath(__file__))

sys.path.insert(0, os.path.normpath(os.path.join(current, '..')))

from service import main

if not os.path.exists('temp'):
	os.mkdir('temp')

main()
