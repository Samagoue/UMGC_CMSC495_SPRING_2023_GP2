from flask import render_template, request, redirect, url_for, session, flash
from .models import db, User, Wishlist

# This function handles the wishlist page. If the request is a GET request, it will query the database for the wishlist items created by the user and render the wishlist.html template with the wishlist items. If the request is a POST request, it will delete the item specified by the wish_id from the wishlist.
# The wishlist page is accessed by navigating to /wishlist. The wishlist page can be accessed by any user who is logged in.
def wishlist():
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

# This function handles the add_wish page. If the request is a POST request, it will add the wish to the database and redirect the user to the wishlist page.
def add_wish():
  username = session['username']
  if request.method == 'POST':
      wish = request.form['wish']

      user = User.query.filter_by(username=username).first()
      wishlist = Wishlist(wish=wish, user_id=user.id)
      db.session.add(wishlist)
      db.session.commit()

      flash('Wish added successfully!')
      return redirect(url_for('main.wishlist_route'))

  return render_template('add_wish.html')