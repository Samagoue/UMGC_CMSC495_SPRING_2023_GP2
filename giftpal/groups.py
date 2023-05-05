from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Group, UserGroup

# This code registers a group with a group name and min dollar amount.
# It first checks if the user is logged in, then checks if the group name is already taken, and then adds the group to the database.
# It then queries the group and the user to create a usergroup entry. This links the user and the group by storing a UserGroup entry.
# The user who registers a group is the admin of that group by default. 
def group_register(): 
  group_name = request.form['group_name']
  min_dollar_amount = request.form['min_dollar_amount']

  if 'username' not in session:
      flash('You need to be logged in before you can register a group!')
      return redirect(url_for('main.register_group_route'))

  group_name_exists = Group.query.filter_by(group_name=group_name).first()

  if group_name_exists:
      flash('This group name is already taken!')
      return redirect(url_for('main.register_group'))

  # Add the group information into the database
  new_group = Group(group_name=group_name, min_dollar_amount=min_dollar_amount)

  db.session.add(new_group)
  db.session.commit()

  # Querying group created and logged in user to create a usergroup entry
  query_group = Group.query.filter_by(group_name=group_name).first()
  logged_in_user = User.query.filter_by(username=session['username']).first()

  # Linking user and group by storing a UserGroup entry. User who registers a group should be admin of that group by default
  new_user_group = UserGroup(user_id=logged_in_user.id, group_id=query_group.id, is_admin=True)

  db.session.add(new_user_group)
  db.session.commit()


  flash('Group Registration successful!')
  return redirect(url_for('main.groups'))

# This code allows the user to modify a group they have admin privileges for.
def mod_group(group_id, group, query_group):
    # Update the group information
    if 'group_name' in request.form:
        group.group_name = request.form['group_name']
    if 'min_dollar_amount' in request.form:
        group.min_dollar_amount = request.form['min_dollar_amount']

    user = User.query.filter_by(username=request.form['modify_selected_user']).first()
    if user is not None: 
        if 'modify_selected_user' in request.form:
            action_to_group = request.form['group_modification']
            user_in_group_already = UserGroup.query.filter_by(user_id=user.id, group_id=group_id).first()
            if action_to_group == "add":
                if user_in_group_already is None:
                    new_user_group = UserGroup(user_id=user.id, group_id=query_group.id, is_admin=False)
                    db.session.add(new_user_group)
                    flash('User successfully added to group!')
                else: 
                    flash('User is already in group!')
            else:
                if user_in_group_already is None:
                    flash('User is not in group!')
                else: 
                    if action_to_group == "delete":
                        deleted_user_group = UserGroup.query.filter_by(user_id=user.id, group_id=group_id).first()
                        db.session.delete(deleted_user_group)
                        flash('User successfully deleted from group!')
                    elif action_to_group == "make_admin":
                        user_group = UserGroup.query.filter_by(user_id=user.id, group_id=group_id).first()
                        user_group.is_admin = True
                        flash('User successfully made admin of group!')


    else: 
        flash('User does not exist!')

    db.session.commit()

    return redirect(url_for('main.groups', group_id=group_id))
