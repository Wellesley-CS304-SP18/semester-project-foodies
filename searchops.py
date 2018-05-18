# Created by Megan Shum
# CS304-Final Project
# 2018.05.27
#!/usr/local/bin/python2.7

import sys
import MySQLdb
import dbconn2

# ================================================================
# The functions that do most of the work.

def searchExists(conn, username):
    '''Returns all of the user's pic post from the database in the form of a dictionary'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select username from user where username = %s', [username])
    exists = curs.fetchone()
    return bool(exists)
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
