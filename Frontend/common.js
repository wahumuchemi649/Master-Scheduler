const API_BASE = "http://localhost:5000/api";

// renders the decorative grid on the left panel — a few cells lit up
// like lessons placed on a weekly timetable
function renderTimetableGrid(containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  const total = 36;
  const filled = new Set([2, 8, 9, 15, 21, 27, 28, 33]);
  const filledDim = new Set([3, 14, 20, 26]);

  for (let i = 0; i < total; i++) {
    const cell = document.createElement("span");
    if (filled.has(i)) cell.classList.add("filled");
    else if (filledDim.has(i)) cell.classList.add("filled-dim");
    container.appendChild(cell);
  }
}

function showError(elementId, message) {
  const el = document.getElementById(elementId);
  el.textContent = message;
  el.classList.add("visible");
}

function hideError(elementId) {
  document.getElementById(elementId).classList.remove("visible");
}

// call at the top of any page that requires a logged-in school.
// redirects to login if there's no active session, otherwise returns the school id.
async function requireAuth() {
  try {
    const res = await fetch(`${API_BASE}/auth/me`, { credentials: "include" });
    if (!res.ok) {
      window.location.href = "login.html";
      return null;
    }
    const data = await res.json();
    return data.id;
  } catch (err) {
    window.location.href = "login.html";
    return null;
  }
}