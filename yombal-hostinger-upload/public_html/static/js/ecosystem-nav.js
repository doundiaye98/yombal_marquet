(function () {
  "use strict";

  const header = document.querySelector(".site-header-unified");
  if (!header) return;

  const triggers = Array.from(header.querySelectorAll(".nav-mega-trigger[data-mega]"));
  if (!triggers.length) return;

  const panels = {};
  triggers.forEach((trigger) => {
    const key = trigger.getAttribute("data-mega");
    const panel = document.getElementById(trigger.getAttribute("aria-controls") || "");
    if (key && panel) {
      panels[key] = { trigger, panel, item: trigger.closest(".nav-item--mega") };
    }
  });

  const keys = Object.keys(panels);
  if (!keys.length) return;

  function canHover() {
    return window.matchMedia("(hover: hover) and (min-width: 901px)").matches;
  }

  function closeAll() {
    header.classList.remove("is-mega-open");
    header.removeAttribute("data-mega-open");
    keys.forEach((key) => {
      const { trigger, panel, item } = panels[key];
      if (item) item.classList.remove("is-open");
      panel.hidden = true;
      trigger.setAttribute("aria-expanded", "false");
    });
  }

  function open(key) {
    if (!panels[key]) return;
    keys.forEach((k) => {
      const { trigger, panel, item } = panels[k];
      const on = k === key;
      if (item) item.classList.toggle("is-open", on);
      panel.hidden = !on;
      trigger.setAttribute("aria-expanded", on ? "true" : "false");
    });
    header.classList.add("is-mega-open");
    header.setAttribute("data-mega-open", key);
  }

  function toggle(key) {
    if (header.getAttribute("data-mega-open") === key) closeAll();
    else open(key);
  }

  triggers.forEach((trigger) => {
    const key = trigger.getAttribute("data-mega");
    trigger.addEventListener("click", (e) => {
      e.stopPropagation();
      toggle(key);
    });
    trigger.addEventListener("mouseenter", () => {
      if (canHover()) open(key);
    });
  });

  // Garder le panneau ouvert quand la souris est dessus
  Object.values(panels).forEach(({ panel }) => {
    panel.addEventListener("mouseenter", () => {
      if (!canHover()) return;
      const key = header.getAttribute("data-mega-open");
      if (key) open(key);
    });
  });

  document.addEventListener("click", (e) => {
    if (!header.contains(e.target)) closeAll();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") closeAll();
  });

  header.addEventListener("mouseleave", (e) => {
    if (!canHover()) return;
    const related = e.relatedTarget;
    if (related && header.contains(related)) return;
    closeAll();
  });
})();
