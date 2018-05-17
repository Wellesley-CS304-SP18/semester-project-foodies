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
    curs.execute('select posts.pic, posts.post_id,posts.username, posts.likes, posts.location, posts.description from posts inner join followers on posts.username = followers.following where followers.follower = %s order by time_stamp DESC limit 30', [username])
    posts= curs.fetchall()
    for post in posts:
        comments = getComments(conn,post['post_id'])
        post['comments'] = comments
        iLike = checkLike(conn, username, post['post_id'])
        post['iLike'] = iLike
    return posts

def getExplorePosts(conn):
    '''Returns all of the pics from the people the user follows from the database in the form of a dictionary'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor) # results as Dictionaries
    curs.execute('select posts.pic, posts.post_id,posts.username, posts.likes, posts.location, posts.description from posts order by posts.likes DESC limit 30')
    posts = curs.fetchall()
    return posts

def updateLikes(conn, postid,username):
    '''Returns the number of followers and number of other users the user is following'''
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into likes (post_id, username) values (%s, %s)',[postid,username])
    curs.execute('select COUNT(post_id) from likes where post_id=%s group by post_id' ,[postid])
    count = curs.fetchone()
    likes = count['COUNT(post_id)']
    curs.execute('update posts set likes = %s where post_id = %s',[likes, postid])

def updateUnlikes (conn, postid, username):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('delete from likes where post_id = %s and username = %s',[postid,username])
    curs.execute('select COUNT(post_id) from likes where post_id=%s group by post_id' ,[postid])
    count = curs.fetchone()
    if not count:
        likes = 0; 
    else:
        likes = count['COUNT(post_id)'] 
    curs.execute('update posts set likes = %s where post_id = %s',[likes, postid])


def getnewLikes(conn, postid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select likes from posts where post_id = %s',[postid])
    info = curs.fetchone()
    return info['likes']

def checkLike(conn, username, postid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select * from likes where post_id = %s and username = %s', [postid, username])
    if curs.fetchone():
        return True
    return False

def getComments(conn, postid):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('select username, comment, time_stamp from comments where post_id = %s',[postid])
    return curs.fetchall()

def addComment(conn, username, postid, comment, time_stamp):
    curs = conn.cursor(MySQLdb.cursors.DictCursor)
    curs.execute('insert into comments (username, post_id, comment, time_stamp ) values (%s, %s, %s, %s)', [username, postid, comment, time_stamp])

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
