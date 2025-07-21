var hintIndex = 0;

function confirmDelete() {
  return confirm("Вы уверены, что хотите удалить аккаунт?");
}

function hinweis() {
    var word = document.getElementById('word').textContent.trim();
    var hintText = document.getElementById('hint-text');
    var hintInput = document.getElementById('hinweis_anzal');

    if (hintIndex < word.length) {
        hintText.textContent += word[hintIndex];
        hintIndex++;
        hintInput.value = hintIndex;
    } else {
        alert("Больше подсказок нет.");
    }
}
