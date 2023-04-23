import sqlite3
import os
from flask import g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Create db file if it doesn't exist
def create_db():
    if not os.path.isfile('database/giftpal.db'):
        open('database/giftpal.db', 'w').close()

# Connect to the SQLite database
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect('database/giftpal.db')
        g.sqlite_db.row_factory = sqlite3.Row
    return g.sqlite_db

# Initialize the SQLite database
def init_db():
    create_db()
    conn = get_db()
    with open('../database/schema.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    with open('../database/init.sql', mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()

# Close the database connection at the end of the request
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
