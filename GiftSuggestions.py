import openai
from my_key import API_KEY

openai.api_key = API_KEY
model_engine = "davinci"


def suggest_gifts(age, min_price, num_gifts=5):
    prompt = f"Suggest {num_gifts} gifts for a person aged {age} with a minimum price of {min_price}."
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        temperature=0.7,
        max_tokens=100,
        n=num_gifts
    )
    if response.choices[0].text.strip() == "":
        return []
    return response.choices


def get_user_input(prompt, input_type):
    while True:
        try:
            user_input = input(prompt)
            if input_type == int:
                return int(user_input)
            else:
                return user_input
        except ValueError:
            print("Invalid input. Please enter a valid value.")


def print_gifts(gifts):
    if not gifts:
        print("Sorry, no gifts were found for your criteria.")
    else:
        print("Here are some gift suggestions:")
        for i, gift in enumerate(gifts):
            print("{}) {}".format(i + 1, gift.text.strip()))


def main():
    print("Welcome to the gift suggestion program!")
    age = get_user_input("What is the recipient's age? ", int)
    min_price = get_user_input("What is the minimum price of the gift? ", int)
    num_gifts = get_user_input("How many gift suggestions do you want? ", int)
    gifts = suggest_gifts(age, min_price, num_gifts)
    print_gifts(gifts)


if __name__ == "__main__":
    main()
