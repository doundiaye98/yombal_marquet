/**
 * YOMBAL MARCHE — Ultra JS Animations
 * Charge via base.html (defer). Respecte prefers-reduced-motion et pointer coarse.
 */
document.addEventListener("DOMContentLoaded", () => {
  const mqFine = window.matchMedia("(pointer: fine)");
  const mqReduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  const motionOk = !mqReduce.matches;

  /* ─── Menu mobile + toasts (Flask) ─── */
  const navToggle = document.getElementById("nav-toggle");
  const navMenu = document.getElementById("primary-nav");
  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const open = navMenu.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navMenu.querySelectorAll("a").forEach((a) => {
      a.addEventListener("click", () => {
        navMenu.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  const toastRoot = document.getElementById("toast-root");
  function showToast(msg) {
    if (!toastRoot || !msg) return;
    const el = document.createElement("div");
    el.className = "toast";
    el.textContent = msg;
    toastRoot.appendChild(el);
    requestAnimationFrame(() => el.classList.add("toast--visible"));
    setTimeout(() => {
      el.classList.remove("toast--visible");
      setTimeout(() => el.remove(), 450);
    }, 3200);
  }
  document.querySelectorAll("[data-toast]").forEach((a) => {
    a.addEventListener("click", () => {
      const m = a.getAttribute("data-toast");
      if (m) showToast(m);
    });
  });

  /* ─── CUSTOM CURSOR ─── */
  const dot = document.getElementById("cursor-dot");
  const ring = document.getElementById("cursor-ring");

  if (motionOk && mqFine.matches && dot && ring) {
    let mouseX = 0;
    let mouseY = 0;
    let ringX = 0;
    let ringY = 0;

    document.addEventListener("mousemove", (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
      dot.style.left = mouseX + "px";
      dot.style.top = mouseY + "px";
    });

    function animateRing() {
      ringX += (mouseX - ringX) * 0.14;
      ringY += (mouseY - ringY) * 0.14;
      ring.style.left = ringX + "px";
      ring.style.top = ringY + "px";
      requestAnimationFrame(animateRing);
    }
    animateRing();

    document
      .querySelectorAll("a, button, .svc-card, .float-card, .c-card")
      .forEach((el) => {
        el.addEventListener("mouseenter", () => {
          dot.style.width = "16px";
          dot.style.height = "16px";
          ring.style.width = "56px";
          ring.style.height = "56px";
          ring.style.borderColor = "rgba(200,80,58,0.6)";
        });
        el.addEventListener("mouseleave", () => {
          dot.style.width = "8px";
          dot.style.height = "8px";
          ring.style.width = "36px";
          ring.style.height = "36px";
          ring.style.borderColor = "rgba(200,80,58,0.4)";
        });
      });
  }

  /* ─── SCROLL REVEAL (stagger) ─── */
  if ("IntersectionObserver" in window && motionOk) {
    const revealEls = document.querySelectorAll(".reveal");
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const siblings = Array.from(entry.target.parentNode.children);
            const idx = siblings.indexOf(entry.target);
            setTimeout(() => {
              entry.target.classList.add("visible");
            }, idx * 80);
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    document.querySelectorAll(".reveal").forEach((el) => el.classList.add("visible"));
  }

  /* ─── HERO WORD-BY-WORD ─── */
  if (motionOk) {
    const heroTitle = document.querySelector(".hero-title");
    if (heroTitle) {
      heroTitle.querySelectorAll(".word").forEach((w, i) => {
        w.style.animationDelay = 0.6 + i * 0.12 + "s";
      });
    }
  }

  /* ─── PARALLAX BLOBS ─── */
  if (motionOk) {
    const blobs = document.querySelectorAll(".blob");
    if (blobs.length) {
      window.addEventListener(
        "scroll",
        () => {
          const y = window.scrollY;
          blobs.forEach((b, i) => {
            const speed = 0.08 + i * 0.04;
            b.style.transform = `translateY(${y * speed}px)`;
          });
        },
        { passive: true }
      );
    }
  }

  /* ─── NAVBAR SCROLL STYLE ─── */
  const nav = document.querySelector(".nav");
  if (nav && motionOk) {
    window.addEventListener(
      "scroll",
      () => {
        if (window.scrollY > 60) {
          nav.style.background = "rgba(245,237,224,0.96)";
          nav.style.boxShadow = "0 4px 40px rgba(26,61,43,0.1)";
        } else {
          nav.style.background = "rgba(245,237,224,0.82)";
          nav.style.boxShadow = "none";
        }
      },
      { passive: true }
    );
  }

  /* ─── COUNTERS ─── */
  function animateCounter(el, target, suffix) {
    suffix = suffix || "";
    const duration = 1800;
    const start = performance.now();
    function update(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 4);
      const value = Math.round(eased * target);
      el.textContent = value.toLocaleString("fr-FR") + suffix;
      if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
  }

  if ("IntersectionObserver" in window && motionOk) {
    const counters = document.querySelectorAll("[data-count]");
    const counterIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.dataset.count, 10);
            const suffix = el.dataset.suffix || "";
            if (!Number.isNaN(target)) animateCounter(el, target, suffix);
            counterIO.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((c) => counterIO.observe(c));
  } else {
    document.querySelectorAll("[data-count]").forEach((el) => {
      const target = parseInt(el.dataset.count, 10);
      const suffix = el.dataset.suffix || "";
      if (!Number.isNaN(target)) el.textContent = target.toLocaleString("fr-FR") + suffix;
    });
  }

  /* ─── MAGNETIC BUTTONS ─── */
  if (motionOk && mqFine.matches) {
    document.querySelectorAll(".btn-primary, .btn-gold, .btn-nav").forEach((btn) => {
      btn.addEventListener("mousemove", (e) => {
        const rect = btn.getBoundingClientRect();
        const cx = rect.left + rect.width / 2;
        const cy = rect.top + rect.height / 2;
        const dx = (e.clientX - cx) * 0.25;
        const dy = (e.clientY - cy) * 0.25;
        btn.style.transform = `translate(${dx}px, ${dy}px) translateY(-3px)`;
      });
      btn.addEventListener("mouseleave", () => {
        btn.style.transform = "";
      });
    });
  }

  /**
   * Tilt uniquement sur .svc-card pour ne pas casser les animations CSS des .float-card du hero.
   */
  if (motionOk && mqFine.matches) {
    document.querySelectorAll(".svc-card").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `
        translateY(-12px)
        rotateX(${-y * 8}deg)
        rotateY(${x * 8}deg)
        scale(1.02)
      `;
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
      });
    });
  }

  /* ─── RIPPLE ─── */
  if (motionOk) {
    const rippleStyle = document.createElement("style");
    rippleStyle.textContent =
      "@keyframes rippleOut { to { transform: scale(1); opacity: 0; } }";
    document.head.appendChild(rippleStyle);

    document
      .querySelectorAll(".btn-primary, .btn-gold, .btn-nav, .btn-outline")
      .forEach((btn) => {
        btn.addEventListener("click", (e) => {
          const rect = btn.getBoundingClientRect();
          const ripple = document.createElement("span");
          const size = Math.max(rect.width, rect.height) * 2;
          ripple.style.cssText = [
            "position:absolute",
            `width:${size}px`,
            `height:${size}px`,
            `left:${e.clientX - rect.left - size / 2}px`,
            `top:${e.clientY - rect.top - size / 2}px`,
            "background:rgba(255,255,255,0.25)",
            "border-radius:50%",
            "transform:scale(0)",
            "animation:rippleOut 0.6s ease forwards",
            "pointer-events:none",
          ].join(";");
          btn.style.position = "relative";
          btn.style.overflow = "hidden";
          btn.appendChild(ripple);
          setTimeout(() => ripple.remove(), 700);
        });
      });
  }

  /* ─── SCROLL PROGRESS ─── */
  const bar = document.getElementById("progress-bar");
  if (bar && motionOk) {
    window.addEventListener(
      "scroll",
      () => {
        const scrolled = window.scrollY;
        const total = document.body.scrollHeight - window.innerHeight;
        const pct = total > 0 ? (scrolled / total) * 100 : 0;
        bar.style.width = pct + "%";
      },
      { passive: true }
    );
  }

  /* ─── Contact : ouvre la zone modes de paiement (#modes-paiement) ─── */
  function focusPaymentSection() {
    if (window.location.hash !== "#modes-paiement") return;
    const el = document.getElementById("modes-paiement");
    if (!el) return;
    requestAnimationFrame(() => {
      el.scrollIntoView({
        behavior: motionOk ? "smooth" : "auto",
        block: "start",
      });
      el.classList.add("payment-highlight");
      window.setTimeout(() => el.classList.remove("payment-highlight"), 2600);
    });
  }
  focusPaymentSection();
  window.addEventListener("hashchange", focusPaymentSection);

  /* Si IntersectionObserver ne déclenche pas (viewport atypique), éviter du contenu invisible. */
  window.setTimeout(() => {
    document.querySelectorAll(".reveal:not(.visible)").forEach((el) => el.classList.add("visible"));
  }, 2800);
});
