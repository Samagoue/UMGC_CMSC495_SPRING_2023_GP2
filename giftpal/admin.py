import hashlib
import random
import string
from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Group, Admin, Key
from .utils import hash_password


def set_admin_user():

    # check if an admin account already exists
    admin = Admin.query.filter_by(username='giftpaladmin').first()

    username = "giftpaladmin"
    password = ''.join(random.choices(
        string.ascii_letters + string.digits, k=10))

    # Hash the password
    enc_password = hash_password(password)

    if admin:
        # update the password for the existing admin account
        admin.password = enc_password
    else:
        # create a new admin account
        admin_acct = Admin(username=username, password=enc_password)
        db.session.add(admin_acct)

    db.session.commit()
    print(f"Admin password: {password}")


def register_group():
    group_name = request.form['group_name']
    group_email = request.form['group_email']
    group_password = request.form['group_password']
    confirm_group_password = request.form['confirm_group_password']
    min_dollar_amount = request.form['min_dollar_amount']

    print("I am here")

    # Ensure group password meets complexity requirements
    if len(group_password) < 8:
        flash('The group password must be at least 8 characters long!')
        return redirect(url_for('main.register_group_route'))
    if not any(char.isdigit() for char in group_password):
        flash('The group password must contain at least one digit!')
        return redirect(url_for('main.register_group_route'))
    if not any(char.isupper() for char in group_password):
        flash('The group password must contain at least one uppercase letter!')
        return redirect(url_for('main.register_group_route'))
    if not any(char.islower() for char in group_password):
        flash('The group password must contain at least one lowercase letter!')
        return redirect(url_for('main.register_group_route'))
    if not any(char in ['$', '#', '@'] for char in group_password):
        flash('The group password must contain at least one special character')
        return redirect(url_for('main.register_group_route'))
    if group_password != confirm_group_password:
        flash('The group password do not match!')
        return redirect(url_for('main.register_group_route'))

    # Hash the group password
    hash_group_password = hashlib.sha256(
        group_password.encode('utf-8')).hexdigest()

    # Check if there is a group registered with this email
    # Might want to consider that emails can have multiple groups attached to them
    print("OR Here")

    group_email_exists = Group.query.filter_by(group_email=group_email).first()

    if group_email_exists:
        # probably unnecessary for the group registration as the plan is to allow  multiple
        # emails attached to a group
        flash('A group with this email already exists!')
        return redirect(url_for('main.register_group_route'))

    # Check if group name is available
    print("Maybe Here")

    group_name_exists = Group.query.filter_by(group_name=group_name).first()

    if group_name_exists:
        flash('This group name is already taken!')
        return redirect(url_for('main.register_group_route'))

    print("Just Here")

    # Add the group information into the database
    new_group = Group(group_name=group_name, min_dollar_amount=min_dollar_amount,
                      group_email=group_email, group_password=hash_group_password)
    db.session.add(new_group)
    db.session.commit()
    print("LIES Here")

    flash('Group Registration successful!')
    # the action after group registration bears further thought
    return redirect(url_for('main.register_route'))


def modify_group():
    """
    Render and provide backend for modify group page
    """
    if request.method == 'POST':
        group_name = request.form['group_name']

        # Hash the password
        hash_group_password = hashlib.sha256(
            group_password.encode('utf-8')).hexdigest()

        # Connect to database
        db = get_db()
        curs = db.cursor()

        # Search for the group credentials in the database
        curs.execute("SELECT * FROM groups WHERE name = ? AND password = ?",
                     (group_name, hash_group_password))
        group_name_exist = curs.fetchone()

        # the if statement will need to be worked on
        if group_name_exist:
            session['group_name'] = group_name
            # return redirect(url_for('group_page'))

        # the below two pieces of code will also need to be modified
        flash('Invalid Group Name or Group Password!')
        return redirect(url_for('modify_group'))

    return render_template('modify_group.html')


def setup_keys():
    if request.method == 'POST':
        email_key = request.form['email_key']
        openai_key = request.form['openai_key']

        # check if a key already exists
        existing_key = Key.query.first()

        if existing_key:
            # update the existing key
            if email_key != '':
                existing_key.email = email_key
            if openai_key != '':
                existing_key.openai = openai_key
        else:
            # create a new key entry
            new_key = Key(email=email_key, openai=openai_key)
            db.session.add(new_key)

        db.session.commit()

    keys = Key.query.all()
    return render_template('api_keys.html', keys=keys)
