# Guess The Number
import time
import random

def guess(start, finish):
    picked_number = random.randint(start, finish)
    guess = None

    while picked_number != guess:
        guess = int(input("Enter you guess: "))
        
        if guess > picked_number:
            print("The number you are looking for is smaller than then number you have picked!")
            time.sleep(0.5)
        elif guess < picked_number:
            print("The number you are looking for is bigger than then number you have picked!")
            time.sleep(0.5)
    
    print("You guessed it! Good for you -__-")

guess(0, 10)

# ----------------------------------------------------------------------------------------

# Reverse guessing game(computer guesses our secret number)
# import random

# def computer_guess():
#     start = int(input("What number does the guess start from? "))
#     end = int(input("And what number does it end with? "))
#     print()

#     is_correct_guess = False

#     while not is_correct_guess:
#         guess = random.randint(start, end)
#         guess_was_right = input(f"is it {guess}? ").lower()
#         if guess_was_right == 'yes':
#             is_correct_guess = True
#         else:
#             lower_or_higher = input("is it lower or is it higher from what i guessed? ").lower()
#             if lower_or_higher == "lower":
#                 end = guess - 1
#             else:
#                 start = guess + 1
    
#     print("Yay, i'm so smart!")

# computer_guess()