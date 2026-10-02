async function startGame() {
    const response = await fetch("/api/game/start", {
        method: "POST"
    });

    const data = await response.json();

    console.log(data);

    // Hide main menu
    document.getElementById("main-menu").style.display = "none";

    // Show game screen
    document.getElementById("game-screen").style.display = "block";

    document.getElementById("choice-buttons").style.display = "block";

    // Show score
    document.getElementById("user-score").textContent = data.score.user;
    document.getElementById("computer-score").textContent = data.score.computer;
}


async function playGame(userChoice) {
    const response = await fetch("/api/game/play", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            choice: userChoice
        })
    });

    const data = await response.json();

    console.log(data);

    // Show choices
    document.getElementById("user-choice").textContent = data.user_choice;
    document.getElementById("computer-choice").textContent = data.computer_choice;

    // Show round result
    document.getElementById("result").textContent = data.result;

    // Update score
    document.getElementById("user-score").textContent = data.score.user;
    document.getElementById("computer-score").textContent = data.score.computer;


    // Check if game is over
    if (data.winner) {

        // Hide Rock / Paper / Scissors buttons
        document.getElementById("choice-buttons").style.display = "none";

        // Show winner
        if (data.winner === "user") {
            document.getElementById("winner-message").textContent =
                "You Win! 🎉";
        } else {
            document.getElementById("winner-message").textContent =
                "Computer Wins! 🤖";
        }
    }
}

async function saveGame() {
    const response = await fetch("/api/game/save",{
        method: "POST"
    })

    const data = await response.json();

    console.log(data)
}

async function continueGame() {
    const response = await fetch("/api/game/load", {
        method: "POST"
    });

    const data = await response.json();

    console.log(data);

    if (!response.ok) {
        alert(data.error);
        return;
    }

    // Hide main menu
    document.getElementById("main-menu").style.display = "none";

    // Show game screen
    document.getElementById("game-screen").style.display = "block";

    // Show choice buttons
    document.getElementById("choice-buttons").style.display = "block";

    // Update score
    document.getElementById("user-score").textContent = data.score.user;
    document.getElementById("computer-score").textContent = data.score.computer;

    // Clear old round information
    document.getElementById("user-choice").textContent = "";
    document.getElementById("computer-choice").textContent = "";
    document.getElementById("result").textContent = "";
    document.getElementById("winner-message").textContent = "";
}

async function exitGame() {
    const response = await fetch("/api/game/exit",{
        method: "POST"
    })

    const data = await response.json();

    console.log(data)

    document.getElementById("game-screen").style.display = "none";
    document.getElementById("main-menu").style.display = "block";
    document.getElementById("user-choice").textContent = "";
    document.getElementById("computer-choice").textContent = "";
    document.getElementById("result").textContent = "";
    document.getElementById("winner-message").textContent = "";
}

async function showHistory() {
    const response = await fetch("/api/game/history");

    const data = await response.json();

    console.log(data);

    document.getElementById("main-menu").style.display = "none";
    document.getElementById("game-screen").style.display = "none";

    const historyScreen = document.getElementById("history-screen");
    historyScreen.style.display = "block";

    const historyList = document.getElementById("history-list");

    historyList.innerHTML = "";

    if (data.history.length === 0) {
        historyList.innerHTML = "<p>No games found.</p>";
        return;
    }

    data.history.forEach((game, index) => {

        const gameElement = document.createElement("div");

        gameElement.innerHTML = `
            <h3>Game ${index + 1}</h3>
            <p>Your Score: ${game.user_score}</p>
            <p>Computer Score: ${game.computer_score}</p>
            <p>Winner: ${game.winner}</p>

            <button onclick="deleteHistory(${game.id})">
                Delete
            </button>

            <hr>
        `;

        historyList.appendChild(gameElement);
    });
}

function backToMenu() {
    document.getElementById("history-screen").style.display = "none";
    document.getElementById("main-menu").style.display = "block";
}

async function deleteHistory(gameId) {
    const response = await fetch(`/api/game/history/${gameId}`, {
        method: "DELETE"
    });

    const data = await response.json();

    console.log(data);

    if (!response.ok) {
        alert(data.error);
        return;
    }

    showHistory();
}

async function deleteAllHistory() {
    
    const confirmed = confirm("Are you sure you want to delete all game history?");

    if (!confirmed) {
        return;
    }

    const response = await fetch("/api/game/history", {
        method: "DELETE"
    });

    const data = await response.json();

    console.log(data);

    if (!response.ok) {
        alert(data.error);
        return;
    }

    showHistory();
}