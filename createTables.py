import MySQLdb as mdb
import re

def readIni(settingsFile):
	ini = open(settingsFile)
	settings = {}
	for line in ini:
		parts = re.match("(.*)=(.*)",line)
		if parts != None:
			settings[parts.group(1).strip()] = parts.group(2).strip()

	return settings


def createTable(sqlFile,settings):
	
	query = open(sqlFile,"r").read()

	connection = mdb.connect(settings['dbHost'], settings['dbUser'], settings['dbPw'], settings['dbName'])
	cursor = connection.cursor()

	cursor.execute(query)

	connection.close()

	return

settings = readIni("settings.ini")

print "create tables"
createTable("create_table_rs_prefixes_out.sql",settings)
createTable("create_table_rpki_roa.sql",settings)
createTable("create_table_rs_rpki_validation.sql",settings)