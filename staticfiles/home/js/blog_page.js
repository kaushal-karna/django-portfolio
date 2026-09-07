/* ================================
   Blog Page JavaScript
================================ */

// Card hover motion is now handled entirely in CSS (.blog-card:hover)
// so it's GPU-accelerated, respects prefers-reduced-motion, and
// doesn't fight with the glass-panel box-shadow set in style.css.
// This file is kept as a hook for future blog interactivity
// (e.g. search/filter by category).


// Select all blog cards
const blogCards = document.querySelectorAll(".blog-card");

blogCards.forEach((card) => {
    // When mouse enters the card
    card.addEventListener("mouseenter", () => {
        card.style.transform = "translateY(-8px)";
        card.style.boxShadow = "0 10px 20px rgba(0, 0, 0, 0.15)";
        card.style.transition = "all 0.3s ease";
    });

    // When mouse leaves the card
    card.addEventListener("mouseleave", () => {
        card.style.transform = "translateY(0)";
        card.style.boxShadow = "none";
    });
});



