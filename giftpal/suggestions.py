import openai
import os
from .models import User, Group, Pair

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gift_suggestion(receiver_id, pair_id):
    # Get the receiver's wishlist and group's minimum dollar amount
    receiver = User.query.get(receiver_id)
    wishlist_items = [item.wish for item in receiver.wishlists]
    group = Group.query.join(Pair).filter(Pair.receiver_id == receiver_id).first()
    group_name = group.group_name
    min_dollar_amount = group.min_dollar_amount

    # Format the prompt for the GPT model
    wishlist_text = "\n- ".join(wishlist_items)
    prompt = f"Please suggest a gift for a person that's part of the {group_name} group with the following wishlist:\n- {wishlist_text}\nThe minimum budget is ${min_dollar_amount}. Please keep your suggesstions short and sweet."

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
