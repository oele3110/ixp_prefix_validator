import MySQLdb as mdb
import datetime
import time
import re

dbHost = None
dbUser = None
dbPw = None
dbName = None

def readIni(settingsFile):
	ini = open(settingsFile)
	settings = {}
	for line in ini:
		parts = re.match("(.*)=(.*)",line)
		if parts != None:
			settings[parts.group(1).strip()] = parts.group(2).strip()

	return settings

def fetchUserAsn(table):
	user = {}
	connection = mdb.connect(dbHost, dbUser, dbPw, dbName)
	cursor = connection.cursor()
	query = "SELECT `id`,`autsys` FROM " + table
	cursor.execute(query)
	results = cursor.fetchall()

	for row in results:
		user[row[1]] = row[0]

	connection.close()

	return user


def insert(users,table,filename):

	connection = mdb.connect(dbHost, dbUser, dbPw, dbName)
	cursor = connection.cursor()

	pattern = "AS(\d{1,5})\|(.*)\|AS(\d{1,5})"
	file = open(filename,"r")
	counter = 0

	for line in file:
		counter +=1
		# import only every 100th entry (for testing purposes)
		if counter%100 == 0:
			parts = re.match(pattern,line)
			ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			query = "INSERT INTO " + table + " (`custid`, `timestamp`, `prefix`, `protocol`, `irrdb`, `rs_origin`) VALUES ("+str(users[(int)(parts.group(1))])+",CURRENT_TIMESTAMP,'"+str(parts.group(2))+"',4,0,"+str(parts.group(3))+")"
			#print query
			cursor.execute(query)
		pass
		
	connection.commit()
	connection.close()
		

	return 0

settings = readIni("settings.ini")

dbHost = settings['dbHost']
dbUser = settings['dbUser']
dbPw = settings['dbPw']
dbName = settings['dbName']

print "fetcht user"
users = fetchUserAsn(settings['custTable'])

print "insert data into table"
insert(users,settings['prefixesTable'],settings['dumpFile'])
insert(users,settings['prefixesOutTable'],settings['dumpFile'])


"""
for user in users:
	print str(user) + " - " + str(users[user])
"""

