# Created by Megan Shum
# CS304-Final Project
# 2018.05.27
#!/usr/local/bin/python2.7

import sys
import MySQLdb
import dbconn2

# ================================================================
# The functions that do most of the work.

def retrievePics(conn, username):
    '''Returns all of the user's pic post from the database in the form of a dictionary'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select pic from posts where username = %s', [username])
    return curs.fetchall()

def getFollow(conn, username):
    '''Returns the number of followers and number of other users the user is following'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select count(*) as followers from followers where following = %s', [username])
    info = curs.fetchone()
    return info['followers']

def getFollowing(conn, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select count(*) as following from followers where follower = %s', [username])
    info = curs.fetchone()
    return info['following']

def follow(conn, follower, following):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('insert into followers(follower,following) values (%s, %s)', [follower, following])
	
def unfollow(conn, follower, following):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('delete from followers where follower = %s and following = %s', [follower, following])

def isFollowing(conn, follower, following):
	curs = conn.cursor(MySQLdb.cursors.DictCursor)
	curs.execute('select follower from followers where follower = %s and following = %s', [follower, following])
	info = curs.fetchone()
	if info == None:
		return False
	else:
		return True
	
	
	
# ================================================================
# This starts the ball rolling, *if* the script is run as a script,
# rather than just being imported.

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: {name} nm".format(name=sys.argv[0])
    else:
        DSN = dbconn2.read_cnf()
        DSN['db'] = 'mmm_db'     # the database we want to connect to
        dbconn2.connect(DSN)
        print lookupByNM(sys.argv[1])
