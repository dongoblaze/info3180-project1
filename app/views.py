"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app
from flask import render_template, request, redirect, url_for, flash

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


@app.route('/addprofile/',methods=('GET', 'POST'))
def addprofile():
    """Render the website's about page."""
    form=AddProfile()
    if request.method == 'POST' and form.validate_on_submit():
        if addprofile.validate_on_submit():

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
    
    
        return redirect(url_for('home', fname=fname,lname=lname,gender=gender,  email=email, location=location,biography=biography ))
    return render_template('addprofile.html',form=form)


# Flash errors from the form if validation fails
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
