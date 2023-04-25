from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import User, Event, Wishlist
from .utils import is_valid_date
from .database import db
from .auth import register, login, logout, reset_password, profile

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    """
    Render home page
    """
    return render_template('home.html')

@bp.route('/register', methods=['GET', 'POST'])
def register_route():
    if request.method == 'POST':
        return register()
    return render_template('register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        return login()
    return render_template('login.html')

@bp.route('/logout')
def logout_route():
    return logout()

@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_route():
    if 'username' in session:
        return reset_password()
    else:
        return redirect(url_for('main.login_route'))

@bp.route('/profile')
def profile_route():
    if 'username' in session:
        return profile()
    else:
        return redirect(url_for('main.login_route'))

@bp.route('/events', methods=['GET', 'POST'])
def events():
    """
    Render and provide backend for events page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'GET':
            # Query events table for events created by the user
            user = User.query.filter_by(username=username).first()
            events = Event.query.filter_by(user_id=user.id).all()

            # Render template with events
            return render_template('events.html', events=events)
        if request.method == 'POST':
            # Get the id of the event to delete
            event_id = request.form['event_id']

            # Delete the event from the database
            event = Event.query.get(event_id)
            db.session.delete(event)
            db.session.commit()

            # Query events table for events created by the user
            user = User.query.filter_by(username=username).first()
            events = Event.query.filter_by(user_id=user.id).all()

        return render_template('events.html', events=events)
    else:
        return redirect(url_for('main.login_route'))

@bp.route('/add-event', methods=['GET', 'POST'])
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

            user = User.query.filter_by(username=username).first()
            event = Event(name=name, date=date, type=event_type, user_id=user.id)
            db.session.add(event)
            db.session.commit()

            flash('Event added successfully!')
            return redirect(url_for('main.events'))

        return render_template('add_event.html')
    else:
        return redirect(url_for('main.login_route'))

@bp.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    """
    Render and provide backend for wishlist page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'GET':
            # Query wishlist table for wishes created by the user
            user = User.query.filter_by(username=username).first()
            wishlist = user.wishlists

            # Render template with wishes
            return render_template('wishlist.html', wishlist=wishlist)
        if request.method == 'POST':
            # Get the id of the wish to delete
            wish_id = request.form['wish_id']

            # Delete the wish from the database
            wish = Wishlist.query.get(wish_id)
            db.session.delete(wish)
            db.session.commit()

            # Query wishlist for wishes created by the user
            user = User.query.filter_by(username=username).first()
            wishlist = user.wishlists

        return render_template('wishlist.html', wishlist=wishlist)
    else:
        return redirect(url_for('main.login_route'))

@bp.route('/add-wish', methods=['GET', 'POST'])
def add_wish():
    """
    Render and provide backend for add wish page
    """
    if 'username' in session:
        username = session['username']
        if request.method == 'POST':
            wish = request.form['wish']

            user = User.query.filter_by(username=username).first()
            wishlist = Wishlist(wish=wish, user_id=user.id)
            db.session.add(wishlist)
            db.session.commit()

            flash('Wish added successfully!')
            return redirect(url_for('main.wishlist'))
        
        return render_template('add_wish.html')
    else:
        return redirect(url_for('main.login_route'))


