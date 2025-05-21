
  async function loadTopCats() {
    try {
      const response = await fetch('/top');
      const cats = await response.json();

      const list = document.getElementById('cat-list');
      list.innerHTML = '';

      cats.forEach(cat => {
        const card = document.createElement('div');
        card.className = 'cat-card';

        card.innerHTML = `
          <img src="${cat.image_url}" alt="котик">
          <div class="cat-fact">${cat.fact}</div>
          <div class="cat-votes">❤️ ${cat.votes} голосів</div>
        `;

        list.appendChild(card);
      });
    } catch (e) {
      document.getElementById('cat-list').innerHTML = '<p>Помилка при завантаженні топу 🐾</p>';
    }
  }

  loadTopCats();
