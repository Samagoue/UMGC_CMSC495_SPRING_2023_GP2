"""
This is a Flask application that tracks your loved one's special dates and their wish lists.
This application provides gift exchange suggestions and email reminders of special dates.
"""

import hashlib
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from emailNotification import send_email

def get_secret(secret_name):
    with open('secrets.txt', 'r') as f:
        for line in f:
            name, value = line.strip().split('=')
            if name == secret_name:
                return value
    return None


app = Flask(__name__)
app.secret_key = get_secret('GIFTPAL_KEY')

# Configuration for the database
app.config['DATABASE'] = 'giftpal.db'


def get_db():
    """
    Connect to the SQLite database
    """
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """
    Initialize the SQLite database
    """
    with app.app_context():
        db = get_db()
        db.execute(
            'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                  username TEXT, email, TEXT, password TEXT)')
        db.execute(
            'CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                username TEXT, name TEXT, date TEXT, type TEXT)')
        db.execute(
            'CREATE TABLE IF NOT EXISTS wishlist (id INTEGER PRIMARY KEY AUTOINCREMENT, \
                username TEXT, wish TEXT)')

        db.commit()
        db.close()


@app.before_first_request
def before_first_request():
    """
    Initialize database before first request
    """
    init_db()


@app.route('/')
def home():
    """
    Render home page
    """
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Render and provide backend for account registration page
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Ensure password meets complexity requirements
        if len(password) < 8:
            flash('Password must be at least 8 characters long!')
            return redirect(url_for('register'))
        if not any(char.isdigit() for char in password):
            flash('Password must contain at least one digit!')
            return redirect(url_for('register'))
        if not any(char.isupper() for char in password):
            flash('Password must contain at least one uppercase letter!')
            return redirect(url_for('register'))
        if not any(char.islower() for char in password):
            flash('Password must contain at least one lowercase letter!')
            return redirect(url_for('register'))
        if not any(char in ['$', '#', '@'] for char in password):
            flash('Password must contain at least one special character')
            return redirect(url_for('register'))
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        # Hash the password
        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        db = get_db()
        c = db.cursor()

        # Check if there is an account with this email
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        acctemail = c.fetchone()

        if acctemail:
            flash('An account with this email already exists!')
            return redirect(url_for('register'))

        # Check if username is available
        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        if user:
            flash('This username is already taken!')
            return redirect(url_for('register'))

        # Add the login information the the database
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                  (username, email, hash_password))
        db.commit()

        flash('Registration successful!')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Render and provide backend for account login page
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        # Connect to database
        db = get_db()
        c = db.cursor()

        # Search for the login credentials in the database
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                  (username, hash_password))
        user = c.fetchone()

        if user:
            session['username'] = username
            return redirect(url_for('profile'))

        flash('Invalid username or password!')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile')
def profile():
    """
    Render and provide backend for user profile page
    """
    if 'username' in session:
        username = session['username']

        # Connect to database
        db = get_db()

        # Query users table for the user's email
        c = db.cursor()
        c.execute("SELECT email FROM users WHERE username = ?", (username,))
        email = c.fetchone()[0]

        return render_template('profile.html', username=username, email=email)

    # Redirect to login page if user is not authenticated
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    """
    Log out of the session
    """
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    """
    Render and provide backend for password reset page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            password = request.form['password']
            confirm_password = request.form['confirm_password']
            hash_password = hashlib.sha256(
                password.encode('utf-8')).hexdigest()

            # Check if the username exists in the database
            db = get_db()
            user = db.execute(
                'SELECT * FROM users WHERE username = ?', (username,)).fetchone()
            db.close()

            if user:
                # Update the user's password in the database
                if password == confirm_password:
                    db = get_db()
                    db.execute('UPDATE users SET password = ? WHERE username = ?',
                               (hash_password, username))
                    db.commit()
                    db.close()

                    # Display a success message to the user
                    flash('Your password has been reset!', 'success')
                    return redirect(url_for('login'))
                else:
                    # Display an error message to the user
                    flash('The passwords do not match!', 'error')
            else:
                # Display an error message to the user
                flash('Invalid username!', 'error')

        return render_template('reset_password.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/events', methods=['GET', 'POST'])
def events():
    """
    Render and provide backend for events page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'GET':
            # Connect to database
            db = get_db()

            # Query events table for events created by the user
            c = db.cursor()
            c.execute("SELECT * FROM events WHERE username = ?", (username,))
            events = c.fetchall()

            # Render template with events
            return render_template('events.html', events=events)
        if request.method == 'POST':
            # Get the id of the event to delete
            event_id = request.form['event_id']

            # Connect to database
            db = get_db()

            # Delete the event from the database
            c = db.cursor()
            c.execute('DELETE FROM events WHERE id=?', (event_id,))
            db.commit()

            # Query events table for events created by the user
            c = db.cursor()
            c.execute("SELECT * FROM events WHERE username = ?", (username,))
            events = c.fetchall()

        return render_template('events.html', events=events)
    else:
        return redirect(url_for('login'))


@app.route('/add-event', methods=['GET', 'POST'])
def add_event():
    """
    Render and provide backend for add event page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            name = request.form['name']
            date = request.form['date']
            event_type = request.form['event_type']
            if event_type == 'custom':
                event_type = request.form['custom_event_type']

            db = get_db()
            db.execute('INSERT INTO events (username, name, date, type) VALUES (?, ?, ?, ?)',
                       (username, name, date, event_type))
            db.commit()
            db.close()
            flash('Event added successfully!')
            return redirect(url_for('events'))

        return render_template('add_event.html')
    else:
        return redirect(url_for('login'))


@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    """
    Render and provide backend for wishlist page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'GET':
            # Connect to database
            db = get_db()

            # Query wishlist table for wishes created by the user
            c = db.cursor()
            c.execute("SELECT * FROM wishlist WHERE username = ?", (username,))
            wishlist = c.fetchall()

            # Render template with wishes
            return render_template('wishlist.html', wishlist=wishlist)
        if request.method == 'POST':
            # Get the id of the wish to delete
            wish_id = request.form['wish_id']

            # Connect to database
            db = get_db()

            # Delete the wish from the database
            c = db.cursor()
            c.execute('DELETE FROM wishlist WHERE id=?', (wish_id,))
            db.commit()

            # Query wishlist for wishes created by the user
            c = db.cursor()
            c.execute("SELECT * FROM wishlist WHERE username = ?", (username,))
            wishlist = c.fetchall()

        return render_template('wishlist.html', wishlist=wishlist)
    else:
        return redirect(url_for('login'))


@app.route('/add-wish', methods=['GET', 'POST'])
def add_wish():
    """
    Render and provide backend for add wish page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            wish = request.form['wish']

            db = get_db()
            db.execute('INSERT INTO wishlist (username, wish) VALUES (?, ?)',
                       (username, wish))
            db.commit()
            db.close()
            flash('Wish added successfully!')
            return redirect(url_for('wishlist'))

        return render_template('add_wish.html')
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
