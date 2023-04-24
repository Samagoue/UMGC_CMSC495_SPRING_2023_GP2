import hashlib
from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User
from .utils import is_valid_date

# Render and provide backend for account registration page
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    dob = request.form['dob']

    # Ensure password meets complexity requirements
    if len(password) < 8:
        flash('Password must be at least 8 characters long!')
        return redirect(url_for('main.register_route'))
    if not any(char.isdigit() for char in password):
        flash('Password must contain at least one digit!')
        return redirect(url_for('main.register_route'))
    if not any(char.isupper() for char in password):
        flash('Password must contain at least one uppercase letter!')
        return redirect(url_for('main.register_route'))
    if not any(char.islower() for char in password):
        flash('Password must contain at least one lowercase letter!')
        return redirect(url_for('main.register_route'))
    if not any(char in ['$', '#', '@'] for char in password):
        flash('Password must contain at least one special character')
        return redirect(url_for('main.register_route'))
    if password != confirm_password:
        flash('Passwords do not match!')
        return redirect(url_for('main.register_route'))
    
    # Ensure first name or last name is not empty
    if not first_name or not last_name:
        flash('Please enter your first and last name!')
        return redirect(url_for('main.register_route'))

    # Ensure date of birth is valid
    if not is_valid_date(dob):
        flash('Please enter your date of birth in the format DDMMYYYY!')
        return redirect(url_for('main.register_route'))

    # Hash the password
    hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Check if there is an account with this email
    acctemail = User.query.filter_by(email=email).first()

    if acctemail:
        flash('An account with this email already exists!')
        return redirect(url_for('main.register_route'))

    # Check if username is available
    user = User.query.filter_by(username=username).first()

    if user:
        flash('This username is already taken!')
        return redirect(url_for('main.register_route'))

    # Add the login information to the database
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=hash_password, dob=dob)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful!')
    return redirect(url_for('main.login_route'))

# Render and provide backend for account login page
def login():
    username = request.form['username']
    password = request.form['password']

    # Hash the password
    hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    # Search for the login credentials in the database
    user = User.query.filter_by(username=username, password=hash_password).first()

    if user:
        session['username'] = username
        return redirect(url_for('main.profile_route'))

    flash('Invalid username or password!')
    return redirect(url_for('main.login_route'))

# Log out of the session
def logout():
    session.pop('username', None)
    return redirect(url_for('main.home'))

# Render and provide backend for password reset page
def reset_password():
    username = session['username']
    if request.method == 'POST':
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        hash_password = hashlib.sha256(
            password.encode('utf-8')).hexdigest()

        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()

        if user:
            # Update the user's password in the database
            if password == confirm_password:
                user.password = hash_password
                db.session.commit()

                # Display a success message to the user
                flash('Your password has been reset!', 'success')
                return redirect(url_for('main.login_route'))
            else:
                # Display an error message to the user
                flash('The passwords do not match!', 'error')
        else:
            # Display an error message to the user
            flash('Invalid username!', 'error')
    return render_template('reset_password.html', username=username)
    
# Render and provide backend for user profile page
def profile():    
    username = session['username']
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)