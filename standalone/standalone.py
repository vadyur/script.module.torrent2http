from __future__ import absolute_import

import sys, os

current = os.path.dirname(__file__)

pwd = os.getcwd()

#sys.path.insert(0, os.path.normpath(os.path.join(current, '..')))
sys.path.insert(0, os.path.normpath(os.path.join(current, '..', 'lib')))

from service import main

if not os.path.exists('temp'):
	os.mkdir('temp')

main()
