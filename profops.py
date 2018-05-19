# profops.py
# CS304-Final Project
# Created by: Megan Shum, Maxine Hood, Mina Hattori
# This file handles all the SQL requests needed for the profile page. 

import sys
import MySQLdb
import dbconn2

def retrievePics(conn, username):
    '''Returns all of the user's pic post from the database in the form of a dictionary'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select pic, description from posts where username = %s', [username])
    return curs.fetchall()

def getFollow(conn, username):
    '''Returns the number of followers'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select count(*) as followers from followers where following = %s', [username])
    info = curs.fetchone()
    return info['followers']

def getFollowing(conn, username):
    '''Returns the number of users this user is following'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select count(*) as following from followers where follower = %s', [username])
    info = curs.fetchone()
    return info['following']

def follow(conn, follower, following):
    '''Adds row in follow table to show that a user followed another user'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into followers(follower,following) values (%s, %s)', [follower, following])

def unfollow(conn, follower, following):
    '''Deletes a row in the follow table when a user unfollows another user'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('delete from followers where follower = %s and following = %s', [follower, following])

def isFollowing(conn, follower, following):
    '''Checks if a user is already following another user'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select follower from followers where follower = %s and following = %s', [follower, following])
    info = curs.fetchone()
    return (info is not None)

def numPosts(conn, username):
    '''Returns the total number of posts a user has created'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select count(*) from posts where username=%s',[username])
    return curs.fetchone()['count(*)']

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
