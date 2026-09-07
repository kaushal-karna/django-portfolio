/* ================================
   Main Project JavaScript 
================================ */

document.addEventListener("DOMContentLoaded", () => {
    // Theme Switcher Logic
    const themeToggleBtn = document.getElementById("themeToggle");
    const htmlElement = document.documentElement;

    // Default to dark theme, but respect anything saved previously
    const savedTheme = localStorage.getItem("theme") || "dark";
    htmlElement.setAttribute("data-theme", savedTheme);

    if (themeToggleBtn) {
        // Sync the icon with the theme immediately on load,
        // instead of only updating after the first click
        themeToggleBtn.textContent = savedTheme === "dark" ? "💡" : "🌙";

        themeToggleBtn.addEventListener("click", () => {
            const currentTheme = htmlElement.getAttribute("data-theme");
            const newTheme = currentTheme === "dark" ? "light" : "dark";

            htmlElement.setAttribute("data-theme", newTheme);
            localStorage.setItem("theme", newTheme);
            themeToggleBtn.textContent = newTheme === "dark" ? "💡" : "🌙";
        });
    }

    // Mobile Navigation Drawer Toggle
    const mobileMenuBtn = document.getElementById("mobileMenuBtn");
    const navMenu = document.getElementById("navMenu");

    if (mobileMenuBtn && navMenu) {
        mobileMenuBtn.setAttribute("aria-expanded", "false");
        mobileMenuBtn.addEventListener("click", () => {
            const isOpen = navMenu.classList.toggle("active");
            mobileMenuBtn.setAttribute("aria-expanded", String(isOpen));
        });
    }
});