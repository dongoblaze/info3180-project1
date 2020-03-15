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
 
# @app.route('/profile')
# def profile():
#     """Render website's home page."""
#     date = format_date_joined()
#     return render_template('profile.html',date=date)
def get_uploads():
    uploads = []
    for subdir, dirs, files in os.walk(app.config['UPLOAD_FOLDER']):
        for file in files:
            if not file.startswith('.'): #ignores hidden files on linux
                uploads.append(file)
    return uploads

# @app.route('/profile/<id>', methods=["GET", "POST"])
# def get_profile(id):
    
#     user = UserProfile.query.filter_by(id = id.first())
    
#     if request.method == "GET":
#         file_folder = app.config['UPLOAD_FOLDER']
#         return render_template("view_user.html", user=user)
    
#     elif request.method == "POST":
#         if user is not None:
#             response = make_response(jsonify(id=id, fname=user.fname,lname=user.lname,gender=user.gender, email=user.email,location=user.location, age=user.biography,photo=user.photo,
#             profile_created_on =user.profile_created_on))
#             response.headers['Content-Type'] = 'application/json'            
#             return response
#         else:
#             flash('No User Found', 'danger')
#             return redirect(url_for("home"))
@app.route('/profile/<id>')
def getuserid(id):
    """Render an individual user profile by the specific user's id."""
    userprofile =UserProfile.query.filter_by(id=int(id)).first()
    return render_template('view_user.html', userprofile=userprofile)

# @app.route('/files')
# def files():
#     if not session.get('logged_in'):
#         abort(401)
    
#     files=get_files()
#     return render_template('files.html', files = files)
    
def format_date_joined():
    datetime.datetime.now()
    date_joined = datetime.date(2020, 3, 10)
    return "Joined on "     + date_joined.strftime("%B %d, %Y") 

@app.route('/profile/',methods=('GET', 'POST'))
def profile():
    """Render the website's about page."""
    form=AddProfile()
    if request.method == 'POST' and form.validate_on_submit():
        if form.validate_on_submit():
            file_folder = app.config['UPLOAD_FOLDER']
            fname = form.fname.data
            lname = form.lname.data
            gender = form.gender.data
            email =form.email.data
            location = form.location.data
            biography = form.biography.data
            pic = request.files['photo']
            photo = secure_filename(pic.filename)
            pic.save(os.path.join(file_folder, photo))
        
            flash('File Saved', 'success')
             # generate user_id, username and date
            id = genId(fname, lname)
            date_created = datetime.date.today()
            # NewProfile = UserProfile(request.form['fname'], request.form['lname'],request.form['gender'],request.form['email'], request.files['file'].filename,request.form['biography'], request.form['photo'].filename)
            
            NewProfile = UserProfile(id=id,fname=fname, lname=lname,gender=gender,email=email,location=location, biography=biography, photo=photo,profile_created_on=date_created)

            db.session.add(NewProfile)
            db.session.commit()
        
        return redirect(url_for('profile', fname=fname,lname=lname,gender=gender,  email=email, location=location,biography=biography ))
    return render_template('addprofile.html',form=form)
@app.route('/profiles', methods=["GET", "POST"])
def profiles():
    
    users = UserProfile.query.all()
    user_list = [{ "id": user.id} for user in users]
    
    if request.method == "GET":
        file_folder = app.config['UPLOAD_FOLDER']
        return render_template("profiles.html", users=users)
    
    elif request.method == "POST":
        response = make_response(jsonify({"users": user_list}))                                           
        response.headers['Content-Type'] = 'application/json'            
        return response
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
