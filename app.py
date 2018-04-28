# Created by Megan Shum
# CS304-Final project
# 2018.04.27
#!/usr/local/bin/python2.7

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
app = Flask(__name__)

import sys,os,random
import dbconn2
import profops
import imghdr
import time
import uploadops

@app.route('/upload/', methods = ['GET', 'POST'])
def upload():
    if not request.cookies.get('username'): #I am assuming Maxine will create the cookie once the user logs in
        flash("Please login")
        return redirect(url_for('login')) # i am assuming that Maxine will make this route
    else:
        if request.method == 'GET':
            return render_template('form.html',src='',nm='')
        else:
            try:
                username = request.cookies.get('username')
                description = request.form['description'] # may throw error
                location = request.form['location']
                time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                f = request.files['pic']
                mime_type = imghdr.what(f.stream)
                if mime_type != 'jpeg':
                    raise Exception('Not a JPEG')
                pic = secure_filename(str(nm)+'.jpeg')
                pathname = 'images/'+filename
                f.save(pathname) # saves the contents in a filename
                flash('Upload successful')
                conn = dbconn2.connect(DSN)
                uploadops.uploadPost(conn, username, description, location, time_stamp, pic)
                return render_template('upload.html',
                                       src=url_for('pic',fname=pic)
                                       )
            except Exception as err:
                flash('Upload failed {why}'.format(why=err))
                return render_template('upload.html',
                                        src='')

@app.route('/profile/', methods = ['GET'])
def profile():
    if not request.cookies.get('username'):
        flash("Please login")
        return redirect(url_for('login'))
    else:
        if request.method == 'GET':
            conn = dbconn2.connect(DSN)
            username = request.cookies.get('username')
            followers = profops.getFollow(conn, username)
            following = profops.getFollowing(conn, username)
            pics = profops.retrievePics(conn, username)
            return render_template('profile.html',
                                    username = username,
                                    followers = followers,
                                    following = following,
                                    pics = pics
                                    )

@app.route('/profile/<fname>')
def pic(fname):
    f = secure_filename(fname)
    mime_type = f.split('.')[-1]
    val = send_from_directory(mime_type,f)
    return val
