from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = '2P7dnLFjVohNt6n4aaA3V'

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
            'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
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
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        # Hash the password
        hash_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        db = sqlite3.connect(app.config['DATABASE'])
        c = db.cursor()

        c.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = c.fetchone()

        if user:
            flash('Username already taken')
            return redirect(url_for('register'))

        # Add the login information the the database
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hash_password))
        db.commit()

        flash('Registration successful')
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

        db = sqlite3.connect(app.config['DATABASE'])
        c = db.cursor()

        # Search for the login credentials in the database
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?",
                  (username, hash_password))
        user = c.fetchone()

        if user:
            session['username'] = username
            return redirect(url_for('profile'))

        flash('Invalid username or password')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/profile')
def profile():
    """
    Render and provide backend for user profile page
    """
    if 'username' in session:
        username = session['username']
        return render_template('profile.html', username=username)

    # Redirect to login page if user is not authenticated
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
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
                    flash('Your password has been reset', 'success')
                    return redirect(url_for('login'))
                else:
                    # Display an error message to the user
                    flash('The passwords do not match', 'error')
            else:
                # Display an error message to the user
                flash('Invalid username', 'error')

        return render_template('reset_password.html', username=username)
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
