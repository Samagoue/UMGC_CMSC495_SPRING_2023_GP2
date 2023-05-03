from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Pair, Event, UserEvent

# This is used to display the events created by the user, and to delete events created by the user.
def do_events():
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

      # Render template with events
      return render_template('events.html', events=events)

# This code adds an event to the database. It first gets the event information from the form on the page. 
# If the event type is custom, it gets the custom event type from the form.
# It then gets the user from the database, and creates a new event. 
# Finally, it adds the event to the database and redirects the user to the events page.
def add_events():
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