#!/usr/bin/env python

import sqlite3
import time
import os
import sys
import commands
import syslog

dbfile = "/opt/dionaea/var/dionaea/logsql.sqlite"

sleep = 20

cid = 0
did = 0

def getLastConnId():
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	sql = "select connection from connections order by connection desc limit 1;"
	#sql = "select max(connection) from connections;"
	c.execute(sql)
	id = 0
	for v in c:
		id = v[0]
	c.close()
	print id

	return id

def getLastDownId():
	conn = sqlite3.connect(dbfile)
	c = conn.cursor()
	sql = "select download from downloads order by download desc limit 1;"
	#sql = "select max(download) from downloads;"
	c.execute(sql)
	id = 0
	for v in c:
		id = v[0]
	c.close()
	print id
	return id

def main():
#Remove
	global cid
	global did
	global oldcid
	global olddid



	oldcid = getLastConnId()
	olddid = getLastDownId()

	while True:
		f = open("/var/log/dionaea.log", "a+")



		#Connections
		conn = sqlite3.connect(dbfile)
		c = conn.cursor()
		sql = "select connection,connection_type,connection_transport,connection_protocol,connection_timestamp,local_host,local_port,remote_host,remote_port from connections where connection > %d order by connection desc" % oldcid


		print sql
		c.execute(sql)
		for v in c:
			data = "connection|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (v[0],v[1],v[2],v[3],v[4],v[7],v[8],v[5],v[6])
			print data
			f.write("%s" % data)
			syslog.syslog( data ) 
		try:
			cid = int(v[0])
		except:
			pass
		#print cid
		c.close()
		#downloads
		conn = sqlite3.connect(dbfile)
		c = conn.cursor()
		sql = "select d.download,d.download_url,d.download_md5_hash,c.local_host,c.local_port,c.remote_host,c.remote_port,c.connection_timestamp,c.connection_type,c.connection_transport,c.connection_protocol from downloads as d, connections as c where d.download > %d and d.connection = c.connection order by d.download desc" % olddid
		c.execute(sql)
		for v in c:
			data = "download|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s|%s\n" % (v[0],v[1],v[2],v[5],v[6],v[3],v[4],v[7],v[8],v[9],v[10])
			print data
			f.write(data)
			syslog.syslog( data ) 
		try:
			did = int(v[0])
		except:
			pass
		#print did
		c.close()
		f.close()

		oldcid = getLastConnId()
		olddid = getLastDownId()

		time.sleep(sleep)

#cid = getLastConnId()
#did = getLastDownId()
main()
