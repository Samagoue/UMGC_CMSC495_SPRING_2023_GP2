import sqlite3
import os
from flask import g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
base_dir = os.path.dirname(os.path.abspath(__file__))
dbdir = os.path.join(base_dir, '..', 'database')

# Create db file if it doesn't exist
def create_db():
    os.makedirs(dbdir, exist_ok=True)
    if not os.path.isfile(dbdir + '/giftpal.db'):
        open(dbdir + '/giftpal.db', 'w').close()

# Connect to the SQLite database
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(dbdir + '/giftpal.db')
        g.sqlite_db.row_factory = sqlite3.Row
    return g.sqlite_db

# Initialize the SQLite database
def init_db():
    create_db()
    conn = get_db()
    
    # Get the current directory and build the absolute path to schema.sql and init.sq
    schema_path = os.path.join(base_dir, '..', 'database', 'schema.sql')
    init_path = os.path.join(base_dir, '..', 'database', 'init.sql')

    with open(schema_path, mode='r') as f:
        conn.cursor().executescript(f.read())
    with open(init_path, mode='r') as f:
        conn.cursor().executescript(f.read())
    conn.commit()

# Close the database connection at the end of the request
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
