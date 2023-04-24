from flask import Flask, g
from giftpal.database import db, init_db, close_db
from giftpal.routes import bp as main_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = '2P7dnLFjVohNt6n4aaA3V'
    app.config['DATABASE'] = 'database/giftpal.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/giftpal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True

    with app.app_context():
        init_db()
    app.teardown_appcontext(close_db)

    db.init_app(app)
    app.register_blueprint(main_bp)

    return app