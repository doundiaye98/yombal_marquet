(function () {

  "use strict";



  const header = document.querySelector(".site-header-unified");

  const trigger = document.querySelector(".nav-mega-trigger");

  const megaPanel = document.getElementById("mega-boutique");

  if (!header || !trigger || !megaPanel) return;



  const megaItem = trigger.closest(".nav-item--mega");



  function open() {

    header.classList.add("is-mega-open");

    if (megaItem) megaItem.classList.add("is-open");

    megaPanel.hidden = false;

    trigger.setAttribute("aria-expanded", "true");

  }



  function close() {

    header.classList.remove("is-mega-open");

    if (megaItem) megaItem.classList.remove("is-open");

    megaPanel.hidden = true;

    trigger.setAttribute("aria-expanded", "false");

  }



  function toggle() {

    if (header.classList.contains("is-mega-open")) close();

    else open();

  }



  trigger.addEventListener("click", (e) => {

    e.stopPropagation();

    toggle();

  });



  document.addEventListener("click", (e) => {

    if (!header.contains(e.target)) close();

  });



  document.addEventListener("keydown", (e) => {

    if (e.key === "Escape") close();

  });



  trigger.addEventListener("mouseenter", () => {

    if (window.matchMedia("(hover: hover) and (min-width: 901px)").matches) open();

  });



  header.addEventListener("mouseleave", (e) => {

    if (!window.matchMedia("(hover: hover) and (min-width: 901px)").matches) return;

    const related = e.relatedTarget;

    if (related && header.contains(related)) return;

    close();

  });

})();

