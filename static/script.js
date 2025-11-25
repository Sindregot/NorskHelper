let currentWord = "";
let streak = 0;
let lives = 3;
let personalHighScore = 0;

// Load leaderboard on page load
window.onload = () => {
    fetchLeaderboard();
    getNewWord();
};

function getNewWord() {
    fetch("/get_word")
        .then(response => response.json())
        .then(data => {
            currentWord = data.norwegian;
            document.getElementById("word-box").textContent = currentWord;
            document.getElementById("answer").value = "";
            document.getElementById("feedback").textContent = "";
        });
}

function submitAnswer() {
    const answerInput = document.getElementById("answer");
    const answer = answerInput.value.trim();

    if (!answer) return;

    fetch("/check_answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            answer: answer,
            current_word: currentWord,
            streak: streak,
            lives: lives
        })
    })
    .then(response => response.json())
    .then(data => {
        streak = data.streak;
        lives = data.lives;
        personalHighScore = Math.max(personalHighScore, streak);

        document.getElementById("streak").textContent = `Streak: ${streak}`;
        document.getElementById("lives").textContent = `Lives: ${"❤️".repeat(lives)}`;
        document.getElementById("feedback").textContent = data.correct ? "Correct!" : `Wrong! Correct: ${data.answer}`;

        if (!data.correct && lives === 3) {
            // only update global leaderboard when streak ends
            fetchLeaderboard();
        }

        getNewWord();
    });
}

function fetchLeaderboard() {
    fetch("/get_leaderboard")
        .then(response => response.json())
        .then(data => {
            const lb = document.getElementById("leaderboard");
            lb.innerHTML = "";
            data.leaderboard.forEach(score => {
                const li = document.createElement("li");
                li.textContent = score;
                lb.appendChild(li);
            });
        });
}

// Submit on Enter key
document.getElementById("answer").addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        submitAnswer();
    }
});
