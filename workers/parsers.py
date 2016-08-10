#!/usr/bin/python

def fileParser(filename, **kwargs):
	try:
		return(filename)
	except:
		log.crash()
		return None
