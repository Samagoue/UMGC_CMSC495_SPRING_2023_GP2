from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

from .suggestions import get_gift_suggestion
from .events import add_events, do_events
from .groups import mod_group, group_register
from .wishlist import add_wish, wishlist
from .models import Pair, Group
from .utils import hash_password
from .database import db
from .auth import register, login, logout, reset_password, profile, setup_login
from .admin import setup_keys
from .gift_exchange import match_gift_pairs

bp = Blueprint('main', __name__)


@bp.route('/')
def home():
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
    if 'username' in session:
        return do_events()
    else:
        return redirect(url_for('main.login_route'))


@bp.route('/add-event', methods=['GET', 'POST'])
def add_event():
    if 'username' in session:
        return add_events()
    else:
        return redirect(url_for('main.login_route'))


@bp.route('/wishlist', methods=['GET', 'POST'])
def wishlist_route():
    if 'username' in session:
        return wishlist()
    else:
        return redirect(url_for('main.login_route'))


@bp.route('/add-wish', methods=['GET', 'POST'])
def add_wish_route():
    if 'username' in session:
        return add_wish()
    else:
        return redirect(url_for('main.login_route'))


@bp.route('/groups', methods=['GET'])
def groups():
    if 'username' in session:
        groups = Group.query.all()
        return render_template('groups.html', groups=groups)
    else:
        return redirect(url_for('main.login_route'))


@bp.route('/register-group', methods=['GET', 'POST'])
def register_group():
    if request.method == 'POST':
        group_register()
        flash('Group Registration successful!')
        return redirect(url_for('main.groups'))

    return render_template('register_group.html')


@bp.route('/modify-group/<int:group_id>', methods=['GET', 'POST'])
def modify_group(group_id):
    # Get the group from the database
    group = Group.query.get_or_404(group_id)
    # I'm pretty sure query_group and group are the same thing
    query_group = Group.query.filter_by(id=group_id).first()

    if request.method == 'POST':
        mod_group(group_id, group, query_group)

    return render_template('modify_group.html', group=group)


@bp.route('/groups/<int:group_id>', methods=['GET', 'POST'])
def group_members_pairs(group_id):
    if 'username' in session:
        group = Group.query.get_or_404(group_id)
        pairs = Pair.query.filter_by(group=group).all()
        members = group.users
        if request.method == 'POST':
            if not pairs:
                match_gift_pairs(group_id)
                pairs = Pair.query.filter_by(group=group).all()
        return render_template('group_members_pairs.html', group=group, members=members, pairs=pairs)


@bp.route('/gift_suggestion/<int:receiver_id>/<int:group_id>', methods=['GET'])
def gift_suggestion(receiver_id, group_id):
    # Call your function to get gift suggestion data
    gift_suggestion_data = get_gift_suggestion(receiver_id, group_id)

    # Return the data as a JSON object
    return jsonify(gift_suggestion_data)


@bp.route('/setup-login', methods=['GET', 'POST'])
def setup_login_route():
    if request.method == 'POST':
        return setup_login()
    return render_template('setup_login.html')


@bp.route('/setup-keys', methods=['GET', 'POST'])
def setup_keys_route():
    if session['username'] == 'giftpaladmin':
        return setup_keys()
    else:
        return redirect(url_for('main.setup_login_route'))
