import httplib
import MySQLdb as mdb
import time
import ipaddr


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


# this method transforms the ip-prefix into binary
def toBin(ip, length):
	prefix = prefix = "%032d" % (int(bin(ipaddr.IPv4Network(ip).network)[2:]))
	return prefix[:int(length)]

# this method checks why a route is invalid
def checkValidity(vrpArray, routeAsn, routeBin):
	validity = ""
	for vrpData in vrpArray:
		vrpAsn = vrpData[0]
		vrpMaxLen = vrpData[1]
		vrpBin = vrpData[2]
		
		#Check if length is too great (prefix too specific)
		if (int(vrpAsn) == int(routeAsn)) and (len(routeBin) > int(vrpMaxLen)):
			if (len(vrpBin) == int(vrpMaxLen)):
				validity = "IP"
			else:
				validity = "IQ"
		#Check if AS number mismatches but prefix falls within valid range
		elif (int(vrpAsn) != int(routeAsn)) and (len(routeBin) >= len(vrpBin)) and (len(routeBin) <= int(vrpMaxLen)):
			validity = "IA"
		#Check if both AS does not match and prefix is too specific
		elif (int(vrpAsn) != int(routeAsn)) and (len(routeBin) > int(vrpMaxLen)):
			validity = "IB"
			
		##############################
		#Validity states:            #
		##############################
		#                            #
		# IP = Fixed length exceeded #
		# IQ = Length range exceeded #
		# IA = AS does not match     #
		# IB = Prefix too specific   #
		#      AND AS does not match #
		#  V = Valid                 #
		#  U = Unknown               #
		##############################
	return validity


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

		validityInfo = ""

		id = splitted[0]
		validity = splitted[1]

		values = splitted[2].split(" ")


		valValue = ""

		if validity == '-1':
			valValue = "U"
		elif validity == '0':
			#print string
			valValue = "IV"
			parts = splitted[3].split(',')
			vrpArray = [[] for i in range(len(parts))]
			counter = 0

			for part in parts:

				subPart = part.split(" ")

				vrpArray[counter] = (subPart[0], subPart[3], toBin(subPart[1], subPart[2]))
				counter += 1

			validityInfo = checkValidity(vrpArray, values[2], toBin(values[0], values[1]))

			#sql = "INSERT INTO " + dbTable2 + " (`rs_prefix_id`, `validity`, `info`) VALUES ("+id+", '"+valValue+"', '"+validityInfo+"');"
		
			#cursor.execute(sql)


		elif validity == '1':
			valValue = "V"

		sql = "INSERT INTO " + dbTable2 + " (`rs_prefix_id`, `validity`, `info`) VALUES ("+id+", '"+valValue+"', '"+validityInfo+"');"
		
		cursor.execute(sql)

		#print sql

	connection.commit()
	connection.close()

def main():


	#data = ["189.84.163.0,24,28171,9", "103.10.232.0,24,1285,10", "103.10.232.0,24,1280,12"]

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
