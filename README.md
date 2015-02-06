This is an RPKI extension for IXP Manager

## Usage:

### 1

First install IXP Manager

https://github.com/inex/IXP-Manager

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

