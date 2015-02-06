import re


def readIni(settingsFile):
	ini = open(settingsFile)
	settings = {}
	for line in ini:
		parts = re.match("(.*)=(.*)",line)
		if parts != None:
			settings[parts.group(1).strip()] = parts.group(2).strip()

	return settings

settings = readIni("settings.ini")

print settings
print settings["dbUser"]