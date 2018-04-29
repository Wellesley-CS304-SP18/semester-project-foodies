# This file has all the SQL Queries necessary for app.py

import sys
import MySQLdb
import dbconn2

# Return a boolean whether the id is a valid id or not
# def isValidUserid(conn, id):
# 	curs = conn.cursor(MySQLdb.cursors.DictCursor)
# 	# curs.execute('select name from person where nm=%s', [id])
# 	# all = curs.fetchone()
# 	# if all is None:
# 	#	return False
# 	#else:
# 	#	return True
# # def passwordMatches(conn, id, password):

# # def registeruser(conn, id, password, name, email):

# # def availableUsername(conn, username):

# # def passwordMatches(conn, passwd, comPasswd):

# # def addNewUser(conn, name, email, username, password):

# =================================================================

if __name__ == '__main__':
		DSN = dbconn2.read_cnf()
		DSN['db'] = 'mhood_db'     # the database we want to connect to
		dbconn2.connect(DSN)