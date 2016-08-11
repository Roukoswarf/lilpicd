#!/usr/bin/python
from config import compressutils, compressargs
from PIL import Image
from subprocess import call, DEVNULL

# Compresses major image filetypes with the tools configured
def dyncompress(filename):
	try:
		with Image.open(filename) as imgfile:
			filetype = imgfile.format.lower()
		
		for util in compressutils[filetype]:
			args = [arg.format(filename=filename) for arg in compressargs[util]]
			call([util] + args, stdout=DEVNULL)
	
	except:
		import traceback
		traceback.print_exc()
		return None
