"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""
import os,random
from app import app, db
from flask import render_template, request, redirect, url_for, flash,jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from flask_wtf import FlaskForm
from app.models import UserProfile
from werkzeug.utils import secure_filename
import datetime
import time


###
# Routing for your application.
###
from .forms import AddProfile

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")
 
@app.route('/profile')

def profile():
    """Render website's home page."""
    date = format_date_joined()
    return render_template('profile.html',date=date)
def get_uploads():
    uploads = []
    for subdir, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if not file.startswith('.'): #ignores hidden files on linux
                uploads.append(file)
    return uploads


# @app.route('/profiles', methods=['GET','POST']|)
# def profiles():
#     profile_list=[]
    
#     profiles= UserProfile.query.filter_by().all()
    
#     if request.method == 'POST':
#         for profile in profiles:
#             profile_list +=[{'fname':profile.fname,'lname':profile.lname, 'userID':profile.id}]
#         return jsonify(users=profile_list)
#     elif request.method == 'GET':
#         return render_template('profiles.html', profile=profiles)
#     return redirect(url_for('home'))



# def get_files():
#     rootdir = os.getcwd()
#     print (rootdir)
#     fileslist =[]
#     for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
#         for file in files:
#             fileslist.append(os.path.join(subdir, file).split('/')[-1])
#     return fileslist
@app.route('/files')
def files():
    if not session.get('logged_in'):
        abort(401)
    
    files=get_files()
    return render_template('files.html', files = files)
    
def format_date_joined():
    datetime.datetime.now()
    date_joined = datetime.date(2020, 3, 10)
    return "Joined on "     + date_joined.strftime("%B %d, %Y") 

@app.route('/addprofile/',methods=('GET', 'POST'))
def addprofile():
    """Render the website's about page."""
    form=AddProfile()
    if request.method == 'POST' and form.validate_on_submit():
        if form.validate_on_submit():

            fname = form.fname.data
            lname = form.lname.data
            gender = form.gender.data
            email =form.email.data
            location = form.location.data
            biography = form.biography.data
            photo = form.photo.data
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
            flash('File Saved', 'success')
             # generate user_id, username and date
            id = genId(fname, lname)
            date_created = datetime.date.today()
            # NewProfile = UserProfile(request.form['fname'], request.form['lname'],request.form['gender'],request.form['email'], request.files['file'].filename,request.form['biography'], request.form['photo'].filename)
            
            NewProfile = UserProfile(fname=fname, lname=lname,gender=gender,email=email,location=location, biography=biography, photo=photo,profile_created_on=date_created)

            db.session.add(NewProfile)

            db.session.commit()
        
        return redirect(url_for('profile', fname=fname,lname=lname,gender=gender,  email=email, location=location,biography=biography ))
    return render_template('addprofile.html',form=form)
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if current_user.is_authenticated:
#         # if user is already logged in, just redirect them to our secure page
#         # or some other page like a dashboard
#         return redirect(url_for('profile'))
#     form = LoginForm()
#     if request.method == "POST" and form.validate_on_submit():
#         # change this to actually validate the entire form submission
#         # and not just one field
#          email = form.email.data
#          password = form.password.data

#          user = UserProfile.query.filter_by(email=email).first()


#          flash('Logged in successfully.', 'success')

#          if form.email.data:
#             # Get the username and password values from the form.

#             # using your model, query database for a user based on the username
#             # and password submitted. Remember you need to compare the password hash.
#             # You will need to import the appropriate function to do so.
#             # Then store the result of that query to a `user` variable so it can be
#             # passed to the login_user() method below.

#             # get user id, load into session
#             login_user(user)

#             # remember to flash a message to the user
#             return redirect(url_for("profile"))  # they should be redirected to a secure-page route instead
#     return render_template("login.html", form=form)

#@app.route('/profile/<userid>', methods=['GET', 'POST'])
#def userprofile(userid):
    #json={}
    #user = UserProfile.query.filter_by(id=userid).first()
    #if request.method == 'POST':
       # json={'userid':user.id, 'username':user.username, 'profile_image':user.pic, 'gender':user.gender, 'age':user.age, 'created_on':user.created}
        #return jsonify(json)

    #elif request.method == 'GET' and user:
        #return render_template('individual.html', profile=user)

    #return render_template('profile.html')

# @app.route("/logout")
# @login_required
# def logout():
#     # Logout the user and end the session
#     logout_user()
#     flash('You have been logged out.', 'danger')
#     return redirect(url_for('home'))
# Flash errors from the form if validation fails

def genId(fname, lname):
    nid = []
    for x in fname:
        nid.append(str(ord(x)))
    for x in lname:
        nid.append(str(ord(x)))
    
    random.shuffle(nid)
    
    nid = "".join(nid)
    
    return nid[:7]
    
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')



@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache- rol'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
