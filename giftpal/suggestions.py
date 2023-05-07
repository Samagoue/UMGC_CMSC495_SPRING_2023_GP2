import openai

from .utils import calculate_age
from .models import User, Group, UserGroup, Setup

def get_gift_suggestion(receiver_id, group_id):
    
    openai.api_key = Setup.query.filter_by(id=1).first().openai_key

    # Get the receiver's wishlist and group's minimum dollar amount
    receiver = User.query.get(receiver_id)
    wishlist_items = [item.wish for item in receiver.wishlists]
    age = calculate_age(receiver.dob)

    # Check if the receiver's wishlist is empty
    if not wishlist_items:
        return "A suggestion cannot be made because there are no items on the receiver's wishlist."

    group = Group.query.join(UserGroup).filter(UserGroup.user_id == receiver_id).first()
    group_name = group.group_name
    min_dollar_amount = group.min_dollar_amount

    # Format the prompt for the GPT model
    wishlist_text = "\n- ".join(wishlist_items)
    prompt = f"Please suggest a gift for a person, age {age}, that's part of the {group_name} group with the following wishlist:\n- {wishlist_text}\nThe minimum budget is ${min_dollar_amount}. Please keep your suggesstions short and sweet."
    print(prompt)
    # Send the request to the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        temperature=0.8,
        max_tokens=50,
        n=1,
        stop=None
    )

    # Get the suggested gift from the response
    suggestion = response.choices[0].text.strip()
    return suggestion
