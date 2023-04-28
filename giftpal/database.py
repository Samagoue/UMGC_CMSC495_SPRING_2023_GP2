import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
base_dir = os.path.dirname(os.path.abspath(__file__))
dbdir = os.path.join(base_dir, '..', 'database')

# Create db file if it doesn't exist
def create_db():
    os.makedirs(dbdir, exist_ok=True)
    db_file = os.path.join(dbdir, 'giftpal.db')
    if not os.path.isfile(db_file):
        open(db_file, 'w').close()
