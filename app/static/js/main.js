let currentCat = { image_url: "", fact: "" };

async function loadCat() {
  const img = document.getElementById('cat-image');
  const spinner = document.getElementById('loading-spinner');
  const fact = document.getElementById('cat-fact');

  try {
    spinner.hidden = false;
    img.hidden = true;
    fact.textContent = "Завантаження факту...";

    const response = await fetch('/random_cat');
    const data = await response.json();

    img.src = data.image_url;
    fact.textContent = data.fact;
    currentCat = data;

    img.onload = () => {
      spinner.hidden = true;
      img.hidden = false;
    };
  } catch (err) {
    alert("Не вдалося завантажити кота 🐱");
    spinner.hidden = true;
    img.hidden = false;
  }
}

async function voteCat() {
  try {
    await fetch('/vote', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentCat)
    });

    alert("Голос зараховано! 🐾");
    loadCat();
  } catch (err) {
    alert("Помилка при голосуванні 😿");
  }
}

loadCat();
