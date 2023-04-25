import hashlib
from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Group

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
    return render_template('profile.html', username=user.username, first_name=user.first_name, last_name=user.last_name, email=user.email, dob=user.dob)


def register_group(): 
        group_name = request.form['group_name']
        group_email = request.form['group_email']
        group_password = request.form['group_password']
        confirm_group_password = request.form['confirm_group_password']

        # Ensure group password meets complexity requirements
        if len(group_password) < 8:
            flash('The group password must be at least 8 characters long!')
            return redirect(url_for('register_group'))
        if not any(char.isdigit() for char in group_password):
            flash('The group password must contain at least one digit!')
            return redirect(url_for('register_group'))
        if not any(char.isupper() for char in group_password):
            flash('The group password must contain at least one uppercase letter!')
            return redirect(url_for('register_group'))
        if not any(char.islower() for char in group_password):
            flash('The group password must contain at least one lowercase letter!')
            return redirect(url_for('register_group'))
        if not any(char in ['$', '#', '@'] for char in group_password):
            flash('The group password must contain at least one special character')
            return redirect(url_for('register_group'))
        if group_password != confirm_group_password:
            flash('The group password do not match!')
            return redirect(url_for('register_group'))

        # Hash the group password
        hash_group_password = hashlib.sha256(group_password.encode('utf-8')).hexdigest()

        # Check if there is a group registered with this email
        #Might want to consider that emails can have multiple groups attached to them
        group_email_exists = Group.query.filter_by(group_email=group_email).first()

        if group_email_exists:
            #probably unnecessary for the group registration as the plan is to allow  multiple
            #emails attached to a group
            flash('A group with this email already exists!')
            return redirect(url_for('register_group'))

        # Check if group name is available
        group_name_exists = Group.query.filter_by(group_name=group_name).first()

        if group_name_exists:
            flash('This group name is already taken!')
            return redirect(url_for('register_group'))

        # Add the group information into the database
        new_group = Group(group_name=group_name, group_email=group_email, group_password=hash_group_password)
        db.session.add(new_group)
        db.session.commit()

        flash('Group Registration successful!')
        #the action after group registration bears further thought
        return redirect(url_for('modify_group'))