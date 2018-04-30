# Created by Mina Hattori
# CS304-Final Project
# 2018.05.27
#!/usr/local/bin/python2.7

import sys
import MySQLdb
import dbconn2

# ================================================================
# The functions that do most of the work.

def retrievePics(conn, username):
    '''Returns all of the pics from the people the user follows from the database in the form of a dictionary'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select posts.pic, posts.post_id,posts.username from posts inner join followers on posts.username = followers.following where followers.follower = %s', [username])
    return curs.fetchall()

# def getLikes(conn, postid):
#     '''Returns the number of followers and number of other users the user is following'''
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)

# def getComments(conn, postid):
#     curs = conn.cursor(MySQLdb.cursors.DictCursor)
 


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
