# uploadops.py
# CS304-Final Project
# Created by: Megan Shum, Maxine Hood, Mina Hattori
#!/usr/local/bin/python2.7
# This file handles all the SQL calls for the upload page.

import sys
import MySQLdb
import dbconn2

def uploadPost(conn, username, description, location, time_stamp, pathname):
    '''Inserts post in Posts table'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('insert into posts(username, description, location, time_stamp, pic) values(%s, %s, %s, %s, %s)', [username, description, location, time_stamp, pathname])

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
