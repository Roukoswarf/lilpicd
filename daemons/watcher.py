#!/usr/bin/python
import pyinotify
from config import watchdir
from os import path

# Watcher daemon
def watcher(work_queue, new_file):
	
	# list to ensure we dont pick up our own recent writes
	loopback = []
	
	class EventHandler(pyinotify.ProcessEvent):
		def process_default(self, event):
			if event.pathname not in loopback:
				print('NEW FILE: {}'.format(event.name))
				
				# add to recent event list
				loopback.append(event.pathname)
				
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
