// Remove this line:
const API_BASE = "http://127.0.0.1:8001/api";

// Use the global API_BASE defined in app.js
console.log("auth.js loaded successfully");
console.log("API_BASE in auth.js:", typeof API_BASE !== "undefined" ? API_BASE : "API_BASE is undefined");

// ---------- Register ----------
async function handleRegister(data) {
    try {
        const res = await fetch(`${API_BASE}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || "Registration failed");
        }
        return await res.json();
    } catch (e) {
        console.error("Register failed:", e);
        alert("Register failed: " + e.message);
    }
}

// ---------- Login ----------
async function handleLogin(data) {
    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || "Login failed");
        }
        return await res.json();
    } catch (e) {
        console.error("Login failed:", e);
        alert("Login failed: " + e.message);
    }
}

// ---------- Page Handlers ----------
document.addEventListener("DOMContentLoaded", () => {
  // Register form
  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(registerForm);
      const payload = Object.fromEntries(fd.entries());

      try {
        const res = await handleRegister(payload);

        // Save only what you need in localStorage
        // IMPORTANT: Set admin flag for admin.html check
        if(res.is_staff) {
          localStorage.setItem('is_admin', 'true');
        } else {
          localStorage.setItem('is_admin', 'false');
        }

        alert("Registration successful!");
        window.location.href = "index.html";
      } catch (error) {
        alert("Registration failed: " + error.message);
      }
    });
  }

  // Login form
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const fd = new FormData(loginForm);
      const payload = Object.fromEntries(fd.entries());

      try {
        const res = await handleLogin(payload);

        // Save user info including is_staff
        localStorage.setItem(
          "teach_user",
          JSON.stringify({
            username: res.username,
            is_staff: res.is_staff || false,
          })
        );

        alert("Login successful!");

        // Redirect based on staff flag
        if (res.is_staff) {
          window.location.href = "admin.html"; // <-- admin page
        } else {
          window.location.href = "index.html"; // <-- normal user homepage
        }
      } catch (error) {
        alert("Login failed: " + error.message);
      }
    });
  }
});
