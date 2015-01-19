import MySQLdb as mdb
import datetime
import time
import re

dbHost = 'localhost'
dbUser = 'root'
dbPw = 'skims12345'
dbName = 'ixp'

def fetchUserAsn():
	user = {}
	connection = mdb.connect(dbHost, dbUser, dbPw, dbName)
	cursor = connection.cursor()
	query = "SELECT `id`,`autsys` FROM `cust`"
	cursor.execute(query)
	results = cursor.fetchall()

	for row in results:
		user[row[1]] = row[0]

	connection.close()

	return user


def insert(users):

	connection = mdb.connect(dbHost, dbUser, dbPw, dbName)
	cursor = connection.cursor()

	pattern = "AS(\d{1,5})\|(.*)\|AS(\d{1,5})"
	file = open("bgp-dump2.txt","r")
	#counter = 0

	for line in file:
		#counter +=1
		#if counter%10000 == 0:
		parts = re.match(pattern,line)
		ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
		query = "INSERT INTO `rs_prefixes_out`(`custid`, `timestamp`, `prefix`, `protocol`, `irrdb`, `rs_origin`) VALUES ("+str(users[(int)(parts.group(1))])+",CURRENT_TIMESTAMP,'"+str(parts.group(2))+"',4,0,"+str(parts.group(3))+")"
		#print query
		cursor.execute(query)
		pass
		
	connection.commit()
	connection.close()
		

	return 0


users = fetchUserAsn()
insert(users)

"""
for user in users:
	print str(user) + " - " + str(users[user])
"""

