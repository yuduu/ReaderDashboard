import random

# Preloaded compliments for reduced I/O
preloaded_compliments = []

with open("app/src/util/compliments.txt", 'r') as file:
    preloaded_compliments = [line.strip() for line in file]

def select_random_compliment():
    try:
        return random.choice(preloaded_compliments)
    except IndexError:
        print("No compliments loaded.")
        return ""

if __name__ == "__main__":
    selected_compliment = select_random_compliment()
    if selected_compliment:
        print("Here's your random compliment:")
        print(selected_compliment)
