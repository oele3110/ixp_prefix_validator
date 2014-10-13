import httplib
import MySQLdb as mdb
import time


host = "tanger.imp.fu-berlin.de"
port = 5003

dbHost = 'localhost'
dbUser = 'root'
dbPw = 'skims12345'
dbName = 'ixp'
dbTable = "`rs_prefixes`"
dbTable2 = "`rs_rpki_validation`"

patternNotFound = '-1\|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+(\d+)'
patternInvalid = '0\|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+(\d+)\|(.+)'
patternValid = '1\|(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)\s+(\d+)\|(.+)'


def getData(conn, data):

	#http://tanger.imp.fu-berlin.de:5003/request?prefix=189.84.163.0&length=24&asn=28171

	returnData = []

	for string in data:

		splitted = string.split(",")

		prefix = splitted[0]
		length = splitted[1]
		asn = splitted[2]
		id = splitted[3]

		conn.request("GET", "/request?prefix="+prefix+"&length="+length+"&asn="+asn)

		r1 = conn.getresponse()

		data = r1.read()

		data = str(id) + "|" + data

		returnData.append(data)

	return returnData

def readSql():

	data = []
	connection=mdb.connect(dbHost, dbUser, dbPw, dbName)
	cursor=connection.cursor()
	sql = "SELECT * FROM "+dbTable#+" LIMIT 10"

	cursor.execute(sql)
	results = cursor.fetchall()

	for row in results:
		id = row[0]
		prefix = row[3]
		asn = row[6]

		splitted = prefix.split("/")
		prefix = splitted[0]
		length = splitted[1]

		newString = prefix+","+length+","+str(asn)+","+str(id)

		data.append(newString)

	connection.close()

	return data


def insertSql(data):

	connection=mdb.connect(dbHost, dbUser, dbPw, dbName)
	cursor=connection.cursor()


	for string in data:
		#print string
		
		splitted = string.split("|")

		id = splitted[0]
		validity = splitted[1]


		valValue = ""

		if validity == '-1':
			valValue = "U"
		elif validity == '0':
			valValue = "IV"
		elif validity == '1':
			valValue = "V"

		sql = "INSERT INTO " + dbTable2 + " (`rs_prefix_id`, `validity`, `info`) VALUES ("+id+", '"+valValue+"', '');"
		
		cursor.execute(sql)

	connection.commit()
	connection.close()

def main():


	#data = ["189.84.163.0,24,28171", "103.10.232.0,24,1280"]

	m1 = int(round(time.time() * 1000))
	data = readSql()
	m2 = int(round(time.time() * 1000))

	print "sql fetch: " + str(m2-m1) + " ms"

	conn = httplib.HTTPConnection(host, port)

	m3 = int(round(time.time() * 1000))
	result = getData(conn, data)
	m4 = int(round(time.time() * 1000))

	print "prefix validation: " + str(m4-m3) + " ms"

	conn.close()

	#for string in result:
	#	print string

	m5 = int(round(time.time() * 1000))
	insertSql(result)
	m6 = int(round(time.time() * 1000))
	

	
	
	print "sql insertion: " + str(m6-m5) + " ms"

main()
