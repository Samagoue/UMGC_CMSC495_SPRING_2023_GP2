from flask import Flask, g
from giftpal.database import db, create_db, dbdir
from giftpal.routes import bp as main_bp
from giftpal.admin import set_admin_user
from giftpal.models import User, Admin
from giftpal.scheduler import run_scheduler

def create_app():
    app = Flask(__name__)
    connstr = 'sqlite:///' + dbdir + '/giftpal.db'
    app.secret_key = '2P7dnLFjVohNt6n4aaA3V'
    app.config['DATABASE'] = 'database/giftpal.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = connstr
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    create_db()

    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        # Sets admin password and prints to console
        set_admin_user()
   
    app.register_blueprint(main_bp)

    return app