"use strict";
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".menu-toggle");
  const nav = document.querySelector(".primary-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
    nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
      toggle.setAttribute("aria-expanded", "false"); nav.classList.remove("is-open");
    }));
  }
  document.querySelectorAll("form").forEach((form) => form.addEventListener("submit", (event) => {
    if (!form.checkValidity()) { event.preventDefault(); form.reportValidity(); }
  }));
});
