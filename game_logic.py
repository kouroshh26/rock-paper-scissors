import random

choices = ["rock", "paper", "scissors"]

def play_round(user_choice):
    computer_choice = random.choice(choices)

    if user_choice == "rock" and computer_choice == "scissors" or user_choice == "paper" and computer_choice == "rock" or user_choice == "scissors" and computer_choice == "paper":
        return "user", computer_choice
    elif user_choice == computer_choice :
        return "draw", computer_choice
    else:
        return "computer", computer_choice
