# app.py
# Created by Megan Shum & Maxine Hood & Mina Hattori
# CS304-Final project
# This file runs the app. 
#!/usr/local/bin/python2.7

from flask import (Flask, render_template, make_response, url_for, request,
                   redirect, flash, session, send_from_directory, jsonify)
from werkzeug import secure_filename
app = Flask(__name__)

import bcrypt
import sys,os,random
import dbconn2
import profops
import imghdr
import time
import uploadops
import accounts
import newsfeedOps
import searchops


app.secret_key = 'your secret here'
# replace that with a random key
app.secret_key = ''.join([ random.choice(('ABCDEFGHIJKLMNOPQRSTUVXYZ' +
                                          'abcdefghijklmnopqrstuvxyz' +
                                          '0123456789'))
                           for i in range(20) ])

# This gets us better error messages for certain common request errors
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

#-------------------------------------------------------------------------
# All pages and funcitons for accounts. (Home, Login, Register, logout)
#-------------------------------------------------------------------------

# Displays home page
@app.route('/')
def home():
	return render_template('home.html',
							title='Foodies')

# Process login form
@app.route('/login/', methods=['GET', 'POST'])
def loginProcess():
	# When get, return empty login page
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('newsfeed'))
        return render_template('login.html',
    							title='Login')
    else:
        username = request.form['username']
        passwd = request.form['passwd']
        conn = dbconn2.connect(DSN)
    	# If valid username and password
        if (accounts.validUsername(conn, username)):
            storedHash = accounts.getHashedPassword(conn, username)
            if(bcrypt.hashpw(passwd.encode('utf-8'), storedHash.encode('utf-8')) == storedHash.encode('utf-8')):
				# Save username to the session
				session['username'] = username
				return redirect(url_for('newsfeed'))
            else:
                flash("Login failed. Please try again")
                return render_template('login.html',
            							title='Login')
        else:
            flash("Invalid username. Please try again")
            return render_template('login.html',
                                    title='Login')


# Function logs out user and returns to the login page									
@app.route('/logout/')
def logout():
    session.pop('username', None)
    return redirect(url_for('loginProcess'))

# Displays the register page
@app.route('/register/')
def register():
	return render_template('register.html',
							title='Register',
							script=url_for('registerProcess'))

# Process register form
@app.route('/register/', methods=['POST'])
def registerProcess():
	# When get, return empty login page
	if request.method == 'GET':
		return register()
	else:
		name = request.form['name']
		email = request.form['email']
		username = request.form['username']
		passwd = request.form['passwd']
		comPasswd = request.form['comPasswd']
        if((name == "") or (email == "") or (username == "") or (passwd == "") or (comPasswd == "")):
            flash("Please fill out all fields")
            return register()
    	conn = dbconn2.connect(DSN)
    	if (accounts.validUsername(conn, username)):
    		flash("Username is taken")
    		return register()
    	if (passwd != comPasswd):
    		flash("Passwords do not match")
    		return register()
    	# Register new account
    	hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    	# If valid username and password
    	accounts.registerUser(conn, username, hashed, name, email)
    	flash("Registration successful")
    	return redirect(url_for('loginProcess'))


#-------------------------------------------------------------------------
# All pages and funcitons for photos
#-------------------------------------------------------------------------		
		
# Takes the upload data and saves image to database.
@app.route('/upload/', methods = ['GET', 'POST'])
def upload():
    if 'username' not in session:
         flash("Please login")
         return redirect(url_for('loginProcess'))
    else:
        if request.method == 'GET':
            return render_template('upload.html',
                                    profuser = session['username'])
        else:
            try:
                username = session['username']
                description = request.form['description'] # may throw error
                location = request.form['location']
                time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
                f = request.files['pic']
                mime_type = imghdr.what(f.stream)
                if mime_type != 'jpeg':
                    raise Exception('Please upload a jpeg image')
                # generating a unique filename with the use of timestamp
                file = f.filename.split('.')[0]+time_stamp+".jpeg"
                pic = secure_filename(str(file))
                pathname = 'images/'+ pic
                f.save(pathname) # saves the contents in a temporarily in the images folder
                flash('Upload successful')
                conn = dbconn2.connect(DSN)
                uploadops.uploadPost(conn, username, description, location,         time_stamp, pic)
                return render_template('upload.html',
                                       src=url_for('pic',fname=pic),
                                       profuser = session['username']
                                       )
            except Exception as err:
                flash('Upload failed {why}'.format(why=err))
                return render_template('upload.html',
                                        profuser = session['username'])


# Renders images by file name
@app.route('/images/<fname>')
def pic(fname):
    f = secure_filename(fname)
    mime_type = f.split('.')[-1]
    val = send_from_directory('images',f)
    return val
				
#-------------------------------------------------------------------------
# All pages and funcitons for displaying posts (Profile, newsfeed, explore, search)
#-------------------------------------------------------------------------	
				
# Displays the profile for a given username										
@app.route('/profile/<username>', methods = ['GET','POST'])
def profile(username):
    if 'username' not in session:
         flash("Please log in")
         return redirect(url_for('loginProcess'))
    else:
        conn = dbconn2.connect(DSN)
        pics = profops.retrievePics(conn, username)
        numPosts = profops.numPosts(conn, username)
        if request.method == 'GET':
			followers = profops.getFollow(conn, username)
			following = profops.getFollowing(conn, username)
			isFollowing = profops.isFollowing(conn, session['username'], username)
			notUser = True
			if (session['username'] == username):
				notUser = False
			return render_template('profile.html',
									username = username,
									followers = followers,
									following = following,
									pics = pics,
									follow = isFollowing,
									notUser = notUser,
                                    numPosts = numPosts,
                                    profuser = session['username']
									)
        else:
            isfollowing = profops.isFollowing(conn, session['username'], username)
            followers = profops.getFollow(conn, username)
            following = profops.getFollowing(conn, username)
            return render_template('profile.html',
                                    username = username,
                                    followers = followers,
                                    following = following,
                                    pics = pics,
									follow = isfollowing,
									notUser = True,
                                    numPosts = numPosts,
                                    profuser = session['username']
                                    )


# Searches for a username and displays that profile
@app.route('/search/', methods = ["POST"])
def search():
    if 'username' in session:
        if request.method == "POST":
            search = request.form['search']
            if search == "":
                return redirect(url_for('newsfeed'))
            else:
                conn = dbconn2.connect(DSN)
                if searchops.searchExists(conn, search):
                    return redirect(url_for('profile', username = search))
                else:
                    return redirect(url_for('newsfeed',profuser = session['username'] ))
    else:
        flash("Please log in")
        return redirect(url_for('loginProcess'))


# Displays the Newsfeed page
@app.route('/newsfeed/', methods=['GET', 'POST'])
def newsfeed():
    if 'username' in session:
        if request.method == 'GET':
                username = session['username']
                conn = dbconn2.connect(DSN)
                information = newsfeedOps.retrievePics(conn, username)
                if (information != None):
                    return render_template ('newsfeed.html',username = username, posts = information, profuser = session['username'])
                else:
                    flash("Follow people to see pictures on your Newsfeed!")
                    return render_template('newsfeed.html', username = username, posts = None, profuser = session['username'])
        else:
            username = session['username']
            comment = request.form['comment']
            time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
            post_id = request.form['post_id']
            conn = dbconn2.connect(DSN)
            newsfeedOps.addComment(conn, username, post_id, comment, time_stamp)
            return redirect(url_for('newsfeed', profuser = session['username']))
    else:
        return redirect(url_for('loginProcess'))


# Display the explore page
@app.route('/explore/', methods = ['GET'])
def explore():
	# if logged in
    if 'username' in session:
        conn = dbconn2.connect(DSN)
		# Get the top posts in the database
        pics = newsfeedOps.getExplorePosts(conn)
        return render_template('explore.html', pics=pics, profuser = session['username'])
    else:
        flash("Please log in")
        return redirect(url_for('loginProcess'))

#-------------------------------------------------------------------------
# Ajax function
#-------------------------------------------------------------------------	
		
# Ajax function for liking a post
@app.route('/likePostAjax/', methods = ['POST'])
def likePostAjax():
    conn = dbconn2.connect(DSN)
    username = session['username']
    post_id = request.form.get('post_id')
    # update the likes for the post
    newsfeedOps.updateLikes(conn,post_id,username)
    # get the new number movie information
    newLikes = newsfeedOps.getnewLikes(conn,post_id)
    return jsonify({"likes": newLikes})

# Ajax function for unliking a post
@app.route('/unlikePostAjax/', methods = ['POST'])
def unlikePostAjax():
    conn = dbconn2.connect(DSN)
    username = session['username']
    post_id = request.form.get('post_id')
    # update thes likes for the post
    newsfeedOps.updateUnlikes(conn,post_id,username)
    # get the new number movie information
    newLikes = newsfeedOps.getnewLikes(conn,post_id)
    return jsonify({"likes": newLikes})

# Ajax function for following a user
@app.route('/followUserAjax/', methods = ['POST'])
def followUserAjax():
    conn = dbconn2.connect(DSN)
    username = session['username']
    profuser = request.form.get('username')

	# Add follow to database and get new followers count
    profops.follow(conn, username, profuser)
    newfollowers = profops.getFollow(conn, profuser)
    return jsonify({"followers": newfollowers})

# Ajax function for unfollowing a user
@app.route('/unfollowUserAjax/', methods = ['POST'])
def unfollowUserAjax():
    conn = dbconn2.connect(DSN)
    username = session['username']
    profuser = request.form.get('username')

    profops.unfollow(conn, username, profuser)
    newfollowers = profops.getFollow(conn, profuser)
    print (newfollowers)


    return jsonify({"followers": newfollowers})



if __name__ == '__main__':

    if len(sys.argv) > 1:
        # arg, if any, is the desired port number
        port = int(sys.argv[1])
        assert(port>1024)
    else:
        port = os.getuid()
    DSN = dbconn2.read_cnf()
    DSN['db'] = 'mmm_db'
    app.debug = True
    app.run('0.0.0.0',port)
