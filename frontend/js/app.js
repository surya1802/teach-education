console.log("app.js loaded successfully");

const API_BASE = "http://127.0.0.1:8001/api";

// State management
let currentQuiz = {
    subject: null,
    questions: [],
    answers: []
};

// Load subjects
async function loadSubjects() {
    try {
        const response = await fetch(`${API_BASE}/subjects`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const subjects = await response.json();
        displaySubjects(subjects);
    } catch (error) {
        console.error("Error loading subjects:", error);
        document.getElementById("subjects").innerHTML = `
            <li style="color: red;">Error loading subjects: ${error.message}</li>
        `;
    }
}

// Display subjects
function displaySubjects(subjects) {
    const subjectsContainer = document.getElementById("subjects");
    if (!subjects.length) {
        subjectsContainer.innerHTML = '<li>No subjects found</li>';
        return;
    }

    subjectsContainer.innerHTML = subjects.map(subject => `
        <li class="subject-card">
            <h3>${subject.title}</h3>
            <p>${subject.description || 'No description'}</p>
            <button onclick="startQuiz(${subject.id})" class="btn">
                Start ${subject.title}
            </button>
        </li>
    `).join('');
}

// Start quiz
async function startQuiz(subjectId) {
    try {
        const response = await fetch(`${API_BASE}/subjects/${subjectId}/questions`);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const questions = await response.json();

        currentQuiz = {
            subject: subjectId,
            questions: questions,
            answers: []
        };

        document.getElementById("subject-list").classList.add("hidden");
        document.getElementById("quiz-area").classList.remove("hidden");

        displayQuestions(questions);
    } catch (error) {
        console.error("Error starting quiz:", error);
        alert("Error loading quiz questions!");
    }
}

// Display questions
function displayQuestions(questions) {
    const quizForm = document.getElementById("quiz-form");
    quizForm.innerHTML = questions.map((q, index) => `
        <div class="question-block">
            <h4>Question ${index + 1}</h4>
            <p class="question">${q.text}</p>
            ${q.qtype === 'mcq' ? 
                `<div class="options">
                    ${q.choices.map(choice => `
                        <label>
                            <input type="radio" name="q${q.id}" value="${choice}">
                            ${choice}
                        </label>
                    `).join('')}
                </div>` :
                `<input type="text" name="q${q.id}" placeholder="Enter your answer">`
            }
        </div>
    `).join('');
}

// Submit quiz
async function submitQuiz() {
    const user = JSON.parse(localStorage.getItem('teach_user')); // Retrieve logged-in user
    if (!user) {
        alert("Please login first!");
        window.location.href = "login.html";
        return;
    }

    const answers = currentQuiz.questions.map(q => {
        const input = document.querySelector(`[name="q${q.id}"]`);
        return {
            question_id: q.id,
            answer: q.qtype === 'mcq' ? 
                document.querySelector(`[name="q${q.id}"]:checked`)?.value || '' :
                input.value
        };
    });

    try {
        const response = await fetch(`${API_BASE}/submit`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: user.username,  // Include the username field
                subject_id: currentQuiz.subject,
                answers: answers
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Submission failed");
        }

        const result = await response.json();
        displayResults(result);
    } catch (error) {
        console.error("Error submitting quiz:", error);
        alert("Error submitting quiz: " + error.message);
    }
}

// Display results
function displayResults(result) {
    document.getElementById("quiz-area").classList.add("hidden");
    document.getElementById("result-area").classList.remove("hidden");

    document.getElementById("result-summary").innerHTML = `
        <div class="result-box">
            <h3>Quiz Complete!</h3>
            <p class="score">Score: ${result.percentage}%</p>
            <p>Correct: ${result.correct}/${result.total_questions}</p>
        </div>
    `;

    document.getElementById("result-details").innerHTML = result.details.map((d, i) => `
        <li class="question-block ${d.correct ? 'correct' : 'wrong'}">
            <p><strong>Question ${i + 1}</strong></p>
            <p>Your answer: ${d.given_answer}</p>
            <p>Correct answer: ${d.correct_answer}</p>
        </li>
    `).join('');
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    loadSubjects();

    document.getElementById("back-to-subjects").addEventListener("click", () => {
        document.getElementById("quiz-area").classList.add("hidden");
        document.getElementById("subject-list").classList.remove("hidden");
    });

    document.getElementById("submit-quiz-btn").addEventListener("click", submitQuiz);

    document.getElementById("take-again").addEventListener("click", () => {
        document.getElementById("result-area").classList.add("hidden");
        document.getElementById("subject-list").classList.remove("hidden");
    });
});