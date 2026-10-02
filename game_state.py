user_score = 0
computer_score = 0
game_active = False
saved_game = None
game_history = []

def update_score(result):
    global user_score, computer_score
    if result == "user":
        user_score += 1
    elif result == "computer":
        computer_score += 1

def get_score():
    return{
        "user": user_score,
        "computer":computer_score
    }

def check_winner():
    if user_score >= 3:
        return "user"
    elif computer_score >= 3:
        return "computer"
    else:
        return None

def reset_game():
    global user_score, computer_score
    user_score = 0
    computer_score = 0

def start_game():
    global game_active
    game_active = True


def exit_game():
    global game_active
    game_active = False

def is_game_active():
    return game_active

def save_game():
    global saved_game
    saved_game = {
        "user_score": user_score,
        "computer_score": computer_score
    }

def load_game():
    global user_score, computer_score
    if saved_game is None:
        return False

    user_score = saved_game["user_score"]
    computer_score = saved_game["computer_score"]
    return True

def add_to_history():
    game = {
        "user_score": user_score,
        "computer_score": computer_score,
        "winner": check_winner()
    }

    game_history.append(game)

def get_history():
    return game_history

def delete_history(index):
    if index < 0 or index >= len(game_history):
        return False

    game_history.pop(index)
    return True

def set_score(user, computer):
    global user_score, computer_score
    user_score = user
    computer_score = computer

def clear_history():
    game_history.clear()