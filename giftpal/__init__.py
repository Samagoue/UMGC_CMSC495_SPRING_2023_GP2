from flask import Flask, g
from giftpal.database import db, init_db, close_db, dbdir
from giftpal.routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    connstr = 'sqlite:///' + dbdir + '/giftpal.db'
    app.secret_key = '2P7dnLFjVohNt6n4aaA3V'
    app.config['DATABASE'] = 'database/giftpal.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = connstr
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.teardown_appcontext(close_db)
   
    app.register_blueprint(main_bp)

    return app