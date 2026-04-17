/**
 * utils.js — shared helpers loaded on every page
 */

/**
 * Show a toast notification.
 * @param {string} message
 * @param {"info"|"success"|"error"|"warning"} type
 * @param {number} duration  ms before auto-dismiss
 */
function showToast(message, type = "info", duration = 3500) {
  const container = document.getElementById("toasts");
  if (!container) return;

  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  el.textContent = message;
  container.appendChild(el);

  setTimeout(() => {
    el.style.opacity = "0";
    el.style.transition = "opacity 0.3s ease";
    setTimeout(() => el.remove(), 300);
  }, duration);
}
