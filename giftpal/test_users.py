from datetime import datetime
from giftpal import db
from .models import User, Event, Wishlist, Group, Pair, UserEvent, UserGroup

# password1 = 0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e
# password2 = 6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4
# password3 = 5906ac361a137e2d286465cd6588ebb5ac3f5ae955001100bc41577c3d751764

  # Create test users
def test_users():
  test_user_1 = User(first_name='John', last_name='Doe', username='johndoe', email='johndoe@example.com',
                    password='0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', dob='01012000', is_admin=False)

  test_user_2 = User(first_name='Jane', last_name='Doe', username='janedoe', email='janedoe@example.com',
                    password='6cf615d5bcaac778352a8f1f3360d23f02f34ec182e259897fd6ce485d7870d4', dob='02021980', is_admin=False)

  # Add users to the database
  db.session.add(test_user_1)
  db.session.add(test_user_2)

  # Commit changes to the database
  db.session.commit()

  # Create test events
  test_event_1 = Event(user_id=test_user_1.id, name='Birthday Party', date='01012023', type='Birthday')
  test_event_2 = Event(user_id=test_user_2.id, name='Wedding Anniversary', date='02022023', type='Anniversary')

  # Add events to the database
  db.session.add(test_event_1)
  db.session.add(test_event_2)

  # Commit changes to the database
  db.session.commit()

  # Create test wishlists
  test_wishlist_1 = Wishlist(user_id=test_user_1.id, wish='A new laptop')
  test_wishlist_2 = Wishlist(user_id=test_user_2.id, wish='A diamond ring')

  # Add wishlists to the database
  db.session.add(test_wishlist_1)
  db.session.add(test_wishlist_2)

  # Commit changes to the database
  db.session.commit()

  # Create test groups
  test_group_1 = Group(group_name='Family', min_dollar_amount=50)
  test_group_2 = Group(group_name='Friends', min_dollar_amount=100)

  # Add groups to the database
  db.session.add(test_group_1)
  db.session.add(test_group_2)

  # Commit changes to the database
  db.session.commit()

  # Create test pairs
  test_pair_1 = Pair(giver_id=test_user_1.id, receiver_id=test_user_2.id, group_id=test_group_1.id)
  test_pair_2 = Pair(giver_id=test_user_2.id, receiver_id=test_user_1.id, group_id=test_group_2.id)

  # Add pairs to the database
  db.session.add(test_pair_1)
  db.session.add(test_pair_2)

  # Commit changes to the database
  db.session.commit()

  # Create test user_events
  test_user_event_1 = UserEvent(user_id=test_user_1.id, event_id=test_event_1.id)
  test_user_event_2 = UserEvent(user_id=test_user_2.id, event_id=test_event_2.id)

  # Add user_events to the database
  db.session.add(test_user_event_1)
  db.session.add(test_user_event_2)

  # Commit changes to the database
  db.session.commit()

  # Create test user_groups
  test_user_group_1 = UserGroup(user_id=test_user_1.id, group_id=test_group_1.id)
  test_user_group_2 = UserGroup(user_id=test_user_2.id, group_id=test_group_2.id)

  # Add user_groups to the database
  db.session.add(test_user_group_1)
  db.session.add(test_user_group_2)

  # Commit changes to the database
  db.session.commit()

