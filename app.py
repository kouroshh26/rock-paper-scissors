from flask import Flask, render_template, request

from database import (
    cancel_active_game,
    create_tables,
    delete_all_games,
    delete_game,
    get_games,
    get_saved_game,
    save_game,
    update_game,
)
from game_logic import choices, play_round
from game_state import (
    check_winner,
    exit_game,
    get_score,
    is_game_active,
    reset_game,
    set_score,
    update_score,
)
from game_state import (
    start_game as activate_game,
)

app = Flask(__name__)
create_tables()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/game/play", methods=["POST"])
def play():
    data = request.get_json()
    if "choice" not in data:
        return{
            "error":"choice is required"
        }, 400
    
    if not is_game_active():
        return{
            "error": "No active game. Start a new game first"
        }, 400
    
    user_choice = data["choice"]
    current_winner = check_winner()
    if current_winner:
        return{
            "message": "Game Over",
            "winner": current_winner
        }, 400

    if user_choice not in choices:
        return{
            "error":"Invalid choice"
        }, 400
    
    result, computer_choice = play_round(user_choice)
    update_score(result)
    score = get_score()
    winner = check_winner()

    if winner:
        saved_game = get_saved_game()
        if saved_game:
            update_game(
                saved_game[0],
                score["user"],
                score["computer"],
                winner,
                "finished"
            )
        else:
            save_game(
                score["user"],
                score["computer"],
                winner,
                "finished"
            )
        
    return {
        "user_choice": user_choice,
        "computer_choice": computer_choice,
        "result": result,
        "score": score,
        "winner": winner
    }

@app.route("/api/game/start", methods=["POST"])
def start_game():
    cancel_active_game()
    reset_game()
    activate_game()

    score = get_score()

    return{
        "message": "game started",
        "score": score
    }

@app.route("/api/game/exit", methods=["POST"])
def exit_game_api():
    exit_game()

    return {
        "message": "game exited"
    }

@app.route("/api/game/save", methods=["POST"])
def save_game_api():
    if not is_game_active():
        return{
            "error": "No active game to save"
        }, 400

    score = get_score()
    saved_game = get_saved_game()
    if saved_game:
        update_game(
            saved_game[0],
            score["user"],
            score["computer"],
            None,
            "playing"
        )
    else:
        save_game(
            score["user"],
            score["computer"],
            None,
            "playing"
        )
    return{
        "message": "Game saved successfully"
    }

@app.route("/api/game/load", methods=["POST"])
def load_game_api():
    saved_game = get_saved_game()

    if saved_game is None:
        return {
            "error": "No saved game found"
        }, 400

    set_score(saved_game[1], saved_game[2])
    activate_game()
    score = get_score()
    return{
        "message": "Game loaded successfully",
        "score": score
    }

@app.route("/api/game/history", methods=["GET"])
def get_game_history():
    games = get_games()
    history = []

    for game in games:
        history.append({
            "id": game[0],
            "user_score": game[1],
            "computer_score": game[2],
            "winner": game[3]
        })

    return{
        "history": history
    }

@app.route("/api/game/history/<int:game_id>", methods=["DELETE"])
def delete_game_history(game_id):
    deleted = delete_game(game_id)

    if not deleted:
        return {
            "error": "Invalid history index"
        }, 400

    return {
        "message": "Game deleted successfully"
    }

@app.route("/api/game/history", methods=["DELETE"])
def delete_all_history():
    delete_all_games()

    return {
        "message": "All history deleted successfully"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)