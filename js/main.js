
  let currentCat = { image_url: "", fact: "" };

  async function loadCat() {
    try {
      const response = await fetch('/random_cat');
      const data = await response.json();

      document.getElementById('cat-image').src = data.image_url;
      document.getElementById('cat-fact').textContent = data.fact;

      currentCat = data;
    } catch (err) {
      alert("Не вдалося завантажити кота 🐱");
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

  // Завантажити першого кота одразу
  loadCat();
