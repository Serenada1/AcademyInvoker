// Сохраняем прогресс
function saveProgress(score) {
    localStorage.setItem('userScore', score);
}

// Загружаем прогресс
function loadProgress() {
    const score = localStorage.getItem('userScore');
    return score ? parseInt(score, 10) : 0;
}

document.addEventListener('DOMContentLoaded', () => {
    let score = loadProgress();
    document.getElementById('score').innerText = score;

    document.getElementById('addPoint').addEventListener('click', () => {
        score += 1;
        saveProgress(score);
        document.getElementById('score').innerText = score;
    });
});
