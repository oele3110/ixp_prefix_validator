This is an RPKI extension for IXP Manager

## Usage:

### 1

Install IXP Manager (Branch: Production)

https://github.com/oele3110/IXP-Manager/tree/production

Install and run RTR HTTP Server

https://github.com/oele3110/RtrHttpServer

### 2

Go into settings.ini and update your settings

### 3

Create additional tables

<pre>
python createTables.py
</pre>

### 4

Insert data from bgp dump (e.g. bgp-dump.txt)

<pre>
python insert.py
</pre>

### 5

Use prefix validator to validate routes and insert into tables

<pre>
python prefix_validator.py
</pre>

