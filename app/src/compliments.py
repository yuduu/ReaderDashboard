import random

def select_random_compliment(file_path):
    try:
        with open(file_path, 'r') as file:
            compliments = file.readlines()
            compliment = random.choice(compliments)
            return compliment.strip()  # Remove any leading/trailing whitespace
    except FileNotFoundError:
        print("Error: File not found.")

if __name__ == "__main__":
    compliments_file = "app/src/util/compliments.txt"
    selected_compliment = select_random_compliment(compliments_file)
    if selected_compliment:
        print("Here's your random compliment:")
        print(selected_compliment)
