#!/usr/bin/python
from multiprocessing import Pool, Event, Manager, Process
from sys import stderr, exit
from signal import signal, SIGINT, SIGTERM, SIG_IGN
from os import getpid, sched_getaffinity
import time
from config import threads

from workers.compressors import dyncompress
from daemons.watcher import watcher

from functools import partial

# Gets threads with available affinity
def getthreads():
	if threads == 'auto':
		return(len(sched_getaffinity(0)))
	return(threads)

def cleanup(workers, daemon_exit, workers_idle):
	print("STOPPING")
	print("Closed job queue")
	print("Signaling daemons to exit")
	daemon_exit.set()
	print("Waiting for workers to exit")
	workers_idle.wait()
	print("Transfers intermediary shut down.  Good night, sweet prince.")
	exit(0)

# Initialization process for workers
def initworker(thread_number, workers_ready):
	# Ensure workers ignore signals, for they hath only one god.
	signal(SIGINT, SIG_IGN)
	signal(SIGTERM, SIG_IGN)
	
	# The following needs to be done last in each thread init,
	# this way automagically fixes race conditions.
	print('Worker {} ready on PID {}'.format(thread_number.get(), getpid()))
	if thread_number.empty():
		workers_ready.set()

def main():
	manager = Manager()
	# Make queue for processes to grab a thread number from
	# also used so that the last worker knows it's last.
	thread_number = manager.Queue()
	[thread_number.put(t) for t in range(getthreads())]
	
	# Set event for handling worker ready condition
	workers_ready = Event()
	workers_idle = Event()
	workers_idle.set()

	# Set event for handling daemon quit condition for stuff that doesnt exit clean
	daemon_exit = Event()
	
	# Set event for handling new file condition
	new_file = Event()

	# Setup workqueue
	queue = manager.Queue()
	
	print("Starting daemons")
	watcherd = Process(name="watcherd", target=watcher, daemon=True, args=(queue,new_file,))
	watcherd.start()
	
	print("Daemons started.")
	
	print("Initializing workers...")
	workers = Pool(processes=thread_number.qsize(),
				initializer=initworker,
				initargs=(thread_number, workers_ready,))
	workers_ready.wait()
	print("All workers ready")
	
	# Set signal handler on main process
	def exit_handler(signum, frame):
		cleanup(workers, daemon_exit, workers_idle)
	signal(SIGINT, exit_handler)
	signal(SIGTERM, exit_handler)

	# Main loop
	while not daemon_exit.is_set():
		# wait until new file is on queue, forced check every 5 minutes.
		status = new_file.wait(timeout=300.0)
		if status: new_file.clear()
		workers_idle.clear()
		
		# Send to workers
		result = workers.map(dyncompress,[queue.get() for q in range(queue.qsize())])
		print(result)
		
		workers_idle.set()
if __name__ == '__main__':
	main()
