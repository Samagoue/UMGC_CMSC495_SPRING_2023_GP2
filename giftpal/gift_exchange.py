import random
from giftpal.models import db, Pair, Group
from .notification import exchange_notification

def match_gift_pairs(group_id):
    # Get Group
    group = Group.query.get(group_id)
    # Get all users in the group
    users = [ug.user for ug in group.users]

    # Skip groups with less than 2 users
    if len(users) < 2:
        return

    # Shuffle the users within the group to randomize the gift exchange order
    random.shuffle(users)

    # Pair up users within the group
    for i in range(len(users)):
        giver = users[i]
        receiver = users[(i + 1) % len(users)]
        pair = Pair(giver=giver, receiver=receiver, group=group)
        db.session.add(pair)

    # Commit the changes to the database
    db.session.commit()
    
    #get all pairs in the group
    pairs = Pair.query.filter_by(group=group).all()
    exchange_notification(pairs)