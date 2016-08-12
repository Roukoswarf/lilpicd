#!/usr/bin/python
from config import compressutils, compressargs, stripexif, watchdir, writedir
from PIL import Image
from subprocess import call, DEVNULL
from datetime import datetime
from pymongo import MongoClient
from os import path, makedirs
from shutil import move

processed = None

# Strip any extra data via rewriting image cleanly
# NOTE: This may not be the best way, seems a bit heavy
def stripmeta(filename):
	with Image.open(filename) as imgfile:
		data = imgfile.getdata()
		newimg = Image.new(imgfile.mode, imgfile.size)
	newimg.putdata(data)
	newimg.save(filename)

# Prepare write destination, return destination filename
# sourcepath is assumed to be absolute, as it comes from inotify
def prepdest(sourcepath):
	# Pull prefix off the source path
	prefix = path.abspath(watchdir)
	subdirs = path.relpath(path.dirname(sourcepath), prefix)
	# Now we should safely have the subdirs under the watch dir
	
	# Make destination tree
	makedirs(path.join(writedir, subdirs), exist_ok=True)
	destpath = path.join(writedir, subdirs, path.basename(sourcepath))
	
	return(destpath)

# Compresses major image filetypes with the tools configured
def dyncompress(filename):
	try:
		# Throw into db before writes begin to ensure no double-processing
		global processed
		oid = processed.insert_one({'filename': filename, 'date': datetime.utcnow()})
		
		# if configured, move to alternative directory
		if not writedir is None:
			if writedir != watchdir:
				destpath = prepdest(filename)
				move(filename, destpath)
				filename = destpath
		
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
