// Redirect if not logged in as admin
// Check if user is logged in and is admin
const user = JSON.parse(localStorage.getItem('teach_user') || '{}');
if (!user.username || !user.is_staff) {
    alert("Access denied. Admins only.");
    window.location.href = "login.html";
}

const API = "http://127.0.0.1:8001/api";

// load subjects for admin
async function loadAdminSubjects() {
  const res = await fetch(`${API}/admin/subjects`);
  const subjects = await res.json();
  const ul = document.getElementById('admin-subjects');
  ul.innerHTML = '';
  subjects.forEach(s => {
    const li = document.createElement('li');
    li.textContent = `${s.title} (order:${s.order})`;
    ul.appendChild(li);
  });

  // Fill subject choices in new-question-form
  const sel = document.getElementById('new-q-subject');
  sel.innerHTML = subjects.map(s => `<option value="${s.id}">${s.title}</option>`).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  // wire forms
  loadAdminSubjects();

  const newSub = document.getElementById('new-subject-form');
  newSub.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(newSub);
    const payload = { title: fd.get('title'), order: Number(fd.get('order')||0) };
    await fetch(`${API}/admin/subjects`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    loadAdminSubjects();
  });

  const newQ = document.getElementById('new-question-form');
  newQ.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fd = new FormData(newQ);
    const subject_id = Number(fd.get('subject_id'));
    const text = fd.get('text');
    const qtype = fd.get('qtype');
    const choicesText = fd.get('choices') || '';
    const choices = choicesText.split(/\r?\n/).map(s => s.trim()).filter(Boolean);
    const correct_answer = fd.get('correct_answer');

    const payload = { subject_id, text, qtype, choices: qtype==='mcq' ? choices : null, correct_answer };
    await fetch(`${API}/admin/questions`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    loadAdminSubjects();
  });
});
