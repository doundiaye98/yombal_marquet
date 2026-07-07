/**
 * Expérience globale — menu cinématique, reveals, entrée page, tilt cartes
 */
document.addEventListener("DOMContentLoaded", () => {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = window.matchMedia("(pointer: fine)").matches;
  const premium = document.body.classList.contains("site-premium");
  if (!premium) return;

  /* ═══ MENU CINÉMATIQUE (mobile / tablette) ═══ */
  const cineNav = document.getElementById("cine-nav");
  const navToggle = document.getElementById("nav-toggle");
  const mqCine = window.matchMedia("(max-width: 900px)");

  function setCineOpen(open) {
    if (!cineNav || !navToggle || !mqCine.matches) return;
    cineNav.classList.toggle("is-open", open);
    cineNav.setAttribute("aria-hidden", open ? "false" : "true");
    navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    navToggle.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
    document.body.classList.toggle("cine-nav-open", open);
    document.body.style.overflow = open ? "hidden" : "";

    if (open) {
      cineNav.querySelectorAll(".cine-nav__link").forEach((link, i) => {
        link.style.setProperty("--i", i);
        link.classList.remove("is-shown");
        requestAnimationFrame(() => {
          setTimeout(() => link.classList.add("is-shown"), 60 + i * 45);
        });
      });
    }
  }

  if (cineNav && navToggle) {
    navToggle.addEventListener("click", () => {
      if (!mqCine.matches) return;
      setCineOpen(!cineNav.classList.contains("is-open"));
    });
    cineNav.querySelectorAll("[data-cine-close], .cine-nav__link").forEach((el) => {
      el.addEventListener("click", () => setCineOpen(false));
    });
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape") setCineOpen(false);
    });
    mqCine.addEventListener("change", () => {
      if (!mqCine.matches) setCineOpen(false);
    });
  }

  const primaryNav = document.getElementById("primary-nav");
  if (primaryNav) {
    const mqDesktop = window.matchMedia("(min-width: 901px)");
    function syncNavAria() {
      primaryNav.setAttribute("aria-hidden", mqDesktop.matches ? "false" : "true");
    }
    syncNavAria();
    mqDesktop.addEventListener("change", syncNavAria);
  }

  /* ═══ ENTRÉE PAGE ═══ */
  const main = document.getElementById("main-content");
  if (main && !reduce && !document.body.classList.contains("is-preloading")) {
    main.classList.add("page-enter");
    requestAnimationFrame(() => main.classList.add("page-enter--active"));
  }

  /* ═══ REVEALS GLOBAUX ═══ */
  const revealSel = ".xd-reveal, .reveal";
  const reveals = document.querySelectorAll(revealSel);
  if (reveals.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible", "visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: "0px 0px -5% 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible", "visible"));
  }

  /* ═══ TILT CARTES BOUTIQUE ═══ */
  if (fine && !reduce) {
    document.querySelectorAll(".boutique-card").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(900px) rotateX(${-y * 4}deg) rotateY(${x * 4}deg) translateY(-3px)`;
        card.style.setProperty("--shine-x", `${(x + 0.5) * 100}%`);
        card.style.setProperty("--shine-y", `${(y + 0.5) * 100}%`);
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  }
});
