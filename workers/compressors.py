#!/usr/bin/python
from config import compressutils, compressargs
from PIL import Image
from subprocess import call, DEVNULL

# Compresses major image filetypes with the tools configured
def dyncompress(filename):
	try:
		imgfile = Image.open(filename)
		
		for util in compressutils[imgfile.format]:
			call([util].extend(compressargs[util], stdout=DEVNULL)
	
	except:
		import traceback
		traceback.print_exc()
		return None
