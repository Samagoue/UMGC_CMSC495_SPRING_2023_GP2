import hashlib
import random
import string
from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Group, Admin, Setup
from .utils import hash_password, validate_password


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

    # Ensure password meets complexity requirements
    if validate_password(group_password, confirm_group_password) is not None:
        return redirect(url_for('main.register_group_route'))

    # Hash the group password
    hash_group_password = hash_password(group_password)

    # Check if there is a group registered with this email
    # Might want to consider that emails can have multiple groups attached to them
    group_email_exists = Group.query.filter_by(group_email=group_email).first()

    if group_email_exists:
        # probably unnecessary for the group registration as the plan is to allow  multiple
        # emails attached to a group
        flash('A group with this email already exists!')
        return redirect(url_for('main.register_group'))

    group_name_exists = Group.query.filter_by(group_name=group_name).first()

    if group_name_exists:
        flash('This group name is already taken!')
        return redirect(url_for('main.register_group'))

    # Add the group information into the database
    new_group = Group(group_name=group_name, min_dollar_amount=min_dollar_amount,
                      group_email=group_email, group_password=hash_group_password)
    db.session.add(new_group)
    db.session.commit()

    flash('Group Registration successful!')
    # the action after group registration bears further thought
    return redirect(url_for('main.register_route'))


def setup_keys():
    if request.method == 'POST':
        email_addr = request.form['email_addr']
        email_key = request.form['email_key']
        openai_key = request.form['openai_key']

        # check if a key already exists
        existing_key = Setup.query.first()

        if existing_key:
            # update the existing key
            if email_addr != '':
                existing_key.email_addr = email_addr
            if email_key != '':
                existing_key.email_key = email_key
            if openai_key != '':
                existing_key.openai_key = openai_key
        else:
            # create a new key entry
            new_key = Setup(email_addr=email_addr, email_key=email_key, openai_key=openai_key)
            db.session.add(new_key)

        db.session.commit()

    keys = Setup.query.all()
    return render_template('api_keys.html', keys=keys)
