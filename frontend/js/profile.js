const API = "http://127.0.0.1:8001/api";

document.addEventListener('DOMContentLoaded', async () => {
  const user = (JSON.parse(localStorage.getItem('teach_user') || '{}') || {}).username;
  if(!user) {
    document.getElementById('profile-info').innerHTML = '<p>Please login first.</p>';
    return;
  }

  document.getElementById('profile-info').innerHTML = `<p>User: ${user}</p>`;

  try {
    const resp = await fetch(`${API}/attempts/history?username=${encodeURIComponent(user)}`);
    if(!resp.ok) throw new Error('no history endpoint');
    const attempts = await resp.json();
    renderAttempts(attempts);
  }catch(e){
    document.getElementById('attempts-list').innerHTML = '<li>No history (endpoint not implemented)</li>';
  }
});

function renderAttempts(attempts){
  const ul = document.getElementById('attempts-list');
  ul.innerHTML = '';
  attempts.forEach(a => {
    const li = document.createElement('li');
    li.textContent = `${a.subject_title} - ${a.score}% - ${a.correct}/${a.total_questions} - ${new Date(a.finished_at).toLocaleString()}`;
    ul.appendChild(li);
  });
}
