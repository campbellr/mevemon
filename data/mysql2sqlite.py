# mysql2sqlite: a program written, composed, and directed by danny campbell because sqlite and mysql are apparently too stupid to talk to each other. Possibly too stupid to live. --danny

import MySQLdb
import sqlite3

# dominion dump from here: (mysql singlefile) http://www.eveonline.com/ingameboard.asp?a=topic&threadID=1258009
# didn't use the sqlite singlefile because I only needed a tiny drop of the DB for the skil information. --danny
mysqldb = MySQLdb.connect( user = "root", passwd = "password", db = "dominion_dump" )

# grab all the group types that belong to category type 16. probably shouldn't hardcode these... --danny
mysqlc = mysqldb.cursor()
mysqlc.execute( """SELECT * FROM `invTypes` WHERE `groupID` = 255 OR `groupID` = 256 OR `groupID` = 257 OR `groupID` = 258 OR `groupID` = 266 OR `groupID` = 267 OR `groupID` = 268 OR `groupID` = 269 OR `groupID` = 270 OR `groupID` = 271 OR `groupID` = 272 OR `groupID` = 273 OR `groupID` = 274 OR `groupID` = 275 OR `groupID` = 278 OR `groupID` = 505 OR `groupID` = 989""" )

# grab all rows from the query. --danny
skills = mysqlc.fetchall()

mysqlc.close()

# add error checking, danny! --danny
sqliteconn = sqlite3.connect( '/tmp/invTypes.sqlite' )
sqlitec = sqliteconn.cursor()

# the question marks just fill in the blanks using the tuple --danny
for skill in skills:
    sqlitec.execute( 'INSERT INTO invTypes VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )', skill )

# why don't I need to commit on MySQLdb? --danny
sqliteconn.commit()
sqlitec.close()
