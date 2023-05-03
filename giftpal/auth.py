from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Group, UserGroup, Admin

from giftpal.utils import hash_password, validate_password

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
    if validate_password(password, confirm_password) is not None:
        return redirect(url_for('main.register_route'))
    
    # Ensure first name or last name is not empty
    if not first_name or not last_name:
        flash('Please enter your first and last name!')
        return redirect(url_for('main.register_route'))

    # Hash the password
    enc_password = hash_password(password)

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
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=enc_password, dob=dob)
    db.session.add(new_user)
    db.session.commit()

    flash('Registration successful!')
    return redirect(url_for('main.login_route'))

# Render and provide backend for account login page
def login():
    username = request.form['username']
    password = request.form['password']

    # Hash the password
    enc_password = hash_password(password)

    # Search for the login credentials in the database
    user = User.query.filter_by(username=username, password=enc_password).first()

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
        enc_password = hash_password(password)

        # Check if the username exists in the database
        user = User.query.filter_by(username=username).first()

        if user:
            # Update the user's password in the database
            if password == confirm_password:
                user.password = enc_password
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
    print(username)
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email, dob=user.dob)

def setup_login():
    username = request.form['username']
    password = request.form['password']

    # Hash the password
    enc_password = hash_password(password)

    # Search for the login credentials in the database
    admin = Admin.query.filter_by(username=username, password=enc_password).first()

    if admin:
        session['username'] = username
        return redirect(url_for('main.setup_keys_route'))

    flash('Invalid username or password!')
    return redirect(url_for('main.setup_login_route'))
