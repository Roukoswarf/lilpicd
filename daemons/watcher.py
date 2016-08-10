#!/usr/bin/python
import pyinotify
from config import watchdir
from os import path

# Watcher daemon
def watcher(work_queue, new_file):
	
	class EventHandler(pyinotify.ProcessEvent):
		def process_default(self, event):
			if not event.name.startswith('.'):
				print('NEW FILE: {}'.format(event.name))
				
				work_queue.put(event.pathname)
				new_file.set()
	
	
	wm = pyinotify.WatchManager()
	mask = pyinotify.IN_CLOSE_WRITE | pyinotify.IN_MOVED_TO
	
	handler = EventHandler()
	notifier = pyinotify.Notifier(wm, handler)
	
	wdd = wm.add_watch(watchdir, mask, rec=False)
	
	notifier.loop()
