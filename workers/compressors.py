#!/usr/bin/python
from config import compressutils, compressargs
from PIL import Image
from subprocess import call, DEVNULL
from datetime import datetime
from pymongo import MongoClient

processed = None

# Compresses major image filetypes with the tools configured
def dyncompress(filename):
	try:
		with Image.open(filename) as imgfile:
			filetype = imgfile.format.lower()
		
		for util in compressutils[filetype]:
			args = [arg.format(filename=filename) for arg in compressargs[util]]
			call([util] + args, stdout=DEVNULL)
		
		global processed
		processed.insert_one({'filename': filename, 'date': datetime.utcnow()})
		
	except:
		import traceback
		traceback.print_exc()
		return None
