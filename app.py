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
import accounts
import newsfeedOps

app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

# login page
@app.route('/login/')
def login():
	return render_template('login.html',
							title='Login',
							script=url_for('loginProcess'))
	
# Process login form
@app.route('/login/', methods=['GET', 'POST'])
def loginProcess():
	# When get, return empty login page
    if request.method == 'GET':
        flash("login failed. Please try again")
        return login()
    else:
        username = request.form['username']
        passwd = request.form['passwd']
    conn = dbconn2.connect(DSN)
    password = passwd # Replace this to find the hashed password
	
	# If valid username and password
    if (accounts.isValidUserid(conn, id) and accounts.passwordMatches(conn, username, password)):
        flash("Login succeeded")
		# Save username to a cookie
        resp = make_response(render_template('login.html'))
        resp.set_cookie('username', username)
        return resp
    else:
        flash("login failed; please try again")
        return login()
		
@app.route('/register/')
def register():
	return render_template('register.html',
							title='Register',
							script=url_for('registerProcess'))
							
# Process login form
@app.route('/register/', methods=['POST'])
def registerProcess():
	# When get, return empty login page
	if request.method == 'GET':
		flash("Registration failed. Please try again")
		return register()
	else:
		name = request.form['name']
		email = request.form['email']
		username = request.form['username']
		passwd = request.form['passwd']
		comPasswd = request.form['comPasswd']
			
	conn = dbconn2.connect(DSN)
	
	if (accounts.availableUsername(conn, username)):
		flash("Username is taken")
		register()
	else: 
	
		if (accounts.passwordMatches(conn, passwd, comPasswd)):
			flash("Passwords do not match")
			register()
			
		else:
			password = passwd # Replace this to find the hashed password	
			# If valid username and password
			accounts.addNewUser(conn, name, email, username, password)
			flash("Registration successful")
			return redirect(url_for('login'))
			
@app.route('/upload/', methods = ['GET', 'POST'])
def upload():
    # if not request.cookies.get('username'): #I am assuming Maxine will create the cookie once the user logs in
    #     flash("Please login")
    #     return redirect(url_for('login')) # i am assuming that Maxine will make this route
    # else:
    if request.method == 'GET':
        return render_template('upload.html')
    else:
        try:
            #username = request.cookies.get('username')
            username = 'megan'
            description = request.form['description'] # may throw error
            location = request.form['location']
            time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            f = request.files['pic']
            mime_type = imghdr.what(f.stream)
            if mime_type != 'jpeg':
                raise Exception('Not a JPEG')
            pic = secure_filename(str(f.filename))
            #dir_path = os.path.dirname(os.path.realpath(__file__))
            pathname = 'images/'+ pic
            f.save(pathname) # saves the contents in a temporarily in the images folder
            flash('Upload successful')
            conn = dbconn2.connect(DSN)
            uploadops.uploadPost(conn, username, description, location,         time_stamp, pic)
            #os.remove(pathname) # deletes image
            return render_template('upload.html',
                                   src=url_for('pic',fname=pic)
                                   )
        except Exception as err:
            flash('Upload failed {why}'.format(why=err))
            return render_template('upload.html')

@app.route('/profile/', methods = ['GET'])
def profile():
    # if not request.cookies.get('username'):
    #     flash("Please login")
    #     return redirect(url_for('login'))
    # else:
    if request.method == 'GET':
        conn = dbconn2.connect(DSN)
        #username = request.cookies.get('username')
        username = 'megan'
        followers = profops.getFollow(conn, username)
        following = profops.getFollowing(conn, username)
        pics = profops.retrievePics(conn, username)
        return render_template('profile.html',
                                username = username,
                                followers = followers,
                                following = following,
                                pics = pics
                                )
@app.route('/newsfeed/', methods = ['GET','POST'])
def newsfeed():
    if request.method == 'GET':
        username = 'minaH'
        conn = dbconn2.connect(DSN)
        information = newsfeedOps.retrievePics(conn, username)
        print str(information [0]['username'])
            #post = information['pic']
            #postuser = information['username']
            #postid = information['post_id']
        return render_template ('newsfeed.html',username = username, posts = information)
    # if 'username' in request.cookies:
    #     username = request.cookies.get('username')
    #     information = newsfeed.retrievePiecs(conn, username)
    #     #post = information['pic']
    #     #postuser = information['username']
    #     #postid = information['post_id']

    #     return render_template ('newsfeed.html',username = username, post = information)
    # else:
    #     return redirect (url_for ('login'))

        





# @app.route('/images/<fname>')
# def pic(fname):
#     f = secure_filename(fname)
#     mime_type = f.split('.')[-1]
#     val = send_from_directory('images',f)
#     return val

if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    DSN = dbconn2.read_cnf()
    DSN['db'] = 'mhattori_db'
    app.debug = True
    app.run('0.0.0.0',port)



