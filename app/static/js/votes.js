async function loadVotes() {
  const table = document.getElementById("votes-table");
  try {
    const response = await fetch("/votes");
    const votes = await response.json();

    if (votes.length === 0) {
      table.innerHTML = "<tr><td colspan='3'>Голосів ще нема 😿</td></tr>";
      return;
    }

    table.innerHTML = "";

    votes.forEach(vote => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${new Date(vote.timestamp).toLocaleString()}</td>
        <td><img src="${vote.image_url}" alt="котик" class="big-cat"></td>
        <td>${vote.fact}</td>
      `;
      table.appendChild(row);
    });
  } catch (err) {
    table.innerHTML = "<tr><td colspan='3'>Помилка завантаження</td></tr>";
  }
}

async function clearVotes() {
  const confirmed = confirm("Точно видалити всі голоси?");
  if (!confirmed) return;

  await fetch("/clear_votes", { method: "POST" });
  loadVotes(); // перезавантажуємо таблицю
}

loadVotes();
