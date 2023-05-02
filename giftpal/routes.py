from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import User, Event, Wishlist, UserEvent, UserGroup, Pair, Group
from .utils import hash_password
from .database import db
from .auth import register, login, logout, reset_password, profile, group_register
from .gift_exchange import match_gift_pairs

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

            # Check if the user has any events
            if not events:
                no_events_message = "You have no events."
            else:
                no_events_message = None

            # Render template with events
            return render_template('events.html', events=events, no_events_message=no_events_message)
        if request.method == 'POST':
            # Get the id of the event to delete
            event_id = request.form['event_id']

            # Delete the associated Pairs for the event
            pairs = Pair.query.filter_by(event_id=event_id).all()
            for pair in pairs:
                db.session.delete(pair)

            # Delete the associated UserEvent instances
            user_events = UserEvent.query.filter_by(event_id=event_id).all()
            for user_event in user_events:
                db.session.delete(user_event)

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
            event = Event(name=name, date=date,
                          type=event_type, user_id=user.id)
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


@bp.route('/groups', methods=['GET'])
def groups():
    if 'username' in session:
        groups = Group.query.all()
        return render_template('groups.html', groups=groups)
    else:
        return redirect(url_for('main.login_route'))


@bp.route('/register-group', methods=['GET', 'POST'])
def register_group():
    """
    Render and provide backend for group registration page
    """
    if request.method == 'POST':
        group_register()
        flash('Group Registration successful!')
        return redirect(url_for('main.groups'))

    return render_template('register_group.html')


@bp.route('/modify-group/<int:group_id>', methods=['GET', 'POST'])
def modify_group(group_id):
    """
    Render and provide backend for modify group page
    """
    # Get the group from the database
    group = Group.query.get_or_404(group_id)
    # I'm pretty sure query_goup and group are the same thing
    query_group = Group.query.filter_by(id=group_id).first()


    if request.method == 'POST':
        # Update the group information
        if 'group_name' in request.form:
            group.group_name = request.form['group_name']
        if 'min_dollar_amount' in request.form:
            group.min_dollar_amount = request.form['min_dollar_amount']
        
        logged_in_user = User.query.filter_by(username=session['username']).first()
        logged_in_user_is_admin = UserGroup.query.filter_by(user_id=logged_in_user.id, group_id=query_group.id).first().is_admin
        user = User.query.filter_by(username=request.form['modify_selected_user']).first()
        

        #First if condition checks if the logged in user is an admin of the group in question.
        #Second if condition checks that there is a username in the input field
        # third if condition checks that the user exists in the database (probably unnecessary to have the second condition if we have the third)
        if logged_in_user_is_admin:
            if 'modify_selected_user' in request.form:
                if user is not None: 
                    action_to_group = request.form['group_modification']

                    if action_to_group == "add":
                        new_user_group = UserGroup(user_id=user.id, group_id=query_group.id, is_admin=False)
                        db.session.add(new_user_group)
                    elif action_to_group == "delete":
                        deleted_user_group = UserGroup.query.filter_by(user_id=user.id, group_id=group_id).first()
                        db.session.delete(deleted_user_group)
                    elif action_to_group == "make_admin":
                        user_group = UserGroup.query.filter_by(user_id=user.id, group_id=group_id).first()
                        user_group.is_admin = True
           
        db.session.commit()

        flash('Group updated successfully!')
        return redirect(url_for('main.groups', group_id=group_id))


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
