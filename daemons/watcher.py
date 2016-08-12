#!/usr/bin/python
import pyinotify
from config import watchdir, dbname
from os import path
from pymongo import MongoClient

# Watcher daemon
def watcher(work_queue, new_file):
	mongoconnect = MongoClient('localhost', 27017)
	db = mongoconnect[dbname]
	
	processed = db['images']
	
	class EventHandler(pyinotify.ProcessEvent):
		def process_default(self, event):
			
			# Lookup for past action
			file_history = processed.find_one({'path': event.pathname})
			
			if file_history is None:
				print('NEW FILE: {}'.format(event.name))
				
				# throw into the workqueue
				work_queue.put(event.pathname)
				
				# wake up main thread
				new_file.set()
	
	wm = pyinotify.WatchManager()
	mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO
	
	handler = EventHandler()
	notifier = pyinotify.Notifier(wm, handler)
	
	wdd = wm.add_watch(watchdir, mask, rec=False)
	
	notifier.loop()
