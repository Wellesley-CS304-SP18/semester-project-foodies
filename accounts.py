# accounts.py
# This file has the SQL Queries necessary for login and registration
# Created by Maxine Hood

import sys
import MySQLdb
import dbconn2
import bcrypt
		
def validPassword(conn, username, password):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select password from user where username=%s', [username])
	result = curs.fetchone()
	return (bcrypt.hashpw(password.encode('utf-8'), result['password'].encode('utf-8')) == result['password'].encode('utf-8'))

def getHashedPassword(conn, username):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select password from user where username=%s', [username])
	result = curs.fetchone()
	return result['password']

def registerUser(conn, username, password, name, email):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('insert into user (username, password, name, email) values (%s, %s, %s, %s)', [username, password, name, email])

def validUsername(conn, username):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select username from user where username=%s', [username])
	all = curs.fetchone()
	return (all is not None)

# =================================================================

if __name__ == '__main__':
		DSN = dbconn2.read_cnf()
		DSN['db'] = 'mmm_db'     # the database we want to connect to
		dbconn2.connect(DSN)