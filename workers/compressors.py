#!/usr/bin/python
from config import compressutils, compressargs, stripexif
from PIL import Image
from subprocess import call, DEVNULL
from datetime import datetime
from pymongo import MongoClient

processed = None

# Strip any extra data via rewriting image cleanly
# NOTE: This may not be the best way, seems a bit heavy
def stripmeta(filename):
	with Image.open(filename) as imgfile:
		data = imgfile.getdata()
		newimg = Image.new(imgfile.mode, imgfile.size)
	newimg.putdata(data)
	newimg.save(filename)

# Compresses major image filetypes with the tools configured
def dyncompress(filename):
	try:
		
		# Throw into db before writes begin to ensure no double-processing
		global processed
		oid = processed.insert_one({'filename': filename, 'date': datetime.utcnow()})
		
		# Open image, determine type, and strip exif if desired.
		with Image.open(filename) as imgfile:
			filetype = imgfile.format.lower()
		
		# Strip metadata, if configured
		if stripexif:
			stripmeta(filename)
		
		# Process files using all configured utilities and args
		for util in compressutils[filetype]:
			args = [arg.format(filename=filename) for arg in compressargs[util]]
			call([util] + args, stdout=DEVNULL)
		
	except:
		import traceback
		from bson.objectid import ObjectId
		
		# Remove from processed collection, as something went wrong
		processed.delete_one({'_id': ObjectId(oid.inserted_id)})
		
		traceback.print_exc()
		return None
