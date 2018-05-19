# accounts.py
# CS304-Final Project
# Created by: Megan Shum, Maxine Hood, Mina Hattori
# This file has the SQL Queries necessary for login and registration

import sys
import MySQLdb
import dbconn2
import bcrypt

def validPassword(conn, username, password):
	'''checks if the password is the correct password used to register'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select password from user where username=%s', [username])
	result = curs.fetchone()
	return (bcrypt.hashpw(password.encode('utf-8'), result['password'].encode('utf-8')) == result['password'].encode('utf-8'))

def getHashedPassword(conn, username):
	'''returns the hashed password stored in database identified by username'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select password from user where username=%s', [username])
	result = curs.fetchone()
	return result['password']

def registerUser(conn, username, password, name, email):
	'''registers the given user info in the user database'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('insert into user (username, password, name, email) values (%s, %s, %s, %s)', [username, password, name, email])

def validUsername(conn, username):
	'''return a boolean if the username is found in the database'''
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select username from user where username=%s', [username])
	all = curs.fetchone()
	return (all is not None)

# =================================================================

if __name__ == '__main__':
		DSN = dbconn2.read_cnf()
		DSN['db'] = 'mmm_db'     # the database we want to connect to
		dbconn2.connect(DSN)
