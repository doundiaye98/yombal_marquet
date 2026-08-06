/**
 * Accueil — expérience immersive premium
 * Preloader · split text · scroll pin · parallaxe · tilt · aura curseur
 */
(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const fine = window.matchMedia("(pointer: fine)").matches;
  const hero = document.querySelector(".xd-hero");
  if (!hero) return;

  const body = document.body;

  /* ═══ PRELOADER ═══ */
  function runPreloader(done) {
    const el = document.getElementById("xd-preloader");
    if (!el || reduce || sessionStorage.getItem("yombal_seen")) {
      el?.remove();
      done();
      return;
    }
    body.classList.add("is-preloading");
    const fill = el.querySelector(".xd-preloader__bar-fill");
    const pct = el.querySelector(".xd-preloader__pct");
    let progress = 0;
    const start = performance.now();
    const dur = 2200;

    function tick(now) {
      const t = Math.min((now - start) / dur, 1);
      const ease = t < 0.7 ? t * 1.15 : 0.8 + (t - 0.7) * 0.67;
      progress = Math.min(Math.round(ease * 100), 100);
      if (fill) fill.style.width = progress + "%";
      if (pct) pct.textContent = progress + "%";
      if (t < 1) {
        requestAnimationFrame(tick);
      } else {
        el.classList.add("is-done");
        body.classList.remove("is-preloading");
        sessionStorage.setItem("yombal_seen", "1");
        setTimeout(() => {
          el.remove();
          done();
        }, 700);
      }
    }
    requestAnimationFrame(tick);
  }

  /* ═══ SPLIT TEXT — caractères animés ═══ */
  function splitLines() {
    hero.querySelectorAll("[data-split]").forEach((line) => {
      const text = line.textContent.trim();
      line.textContent = "";
      line.setAttribute("aria-label", text);
      [...text].forEach((ch, i) => {
        const span = document.createElement("span");
        span.className = "xd-char";
        span.style.setProperty("--ci", i);
        span.textContent = ch === " " ? "\u00a0" : ch;
        span.setAttribute("aria-hidden", "true");
        line.appendChild(span);
      });
    });
  }

  function revealHero() {
    hero.querySelectorAll(".xd-char").forEach((ch) => {
      const i = parseInt(ch.style.getPropertyValue("--ci") || "0", 10);
      ch.style.setProperty("--delay", `${0.45 + i * 0.035}s`);
      requestAnimationFrame(() => ch.classList.add("is-in"));
    });
    hero.querySelectorAll(".xd-eyebrow, .xd-hero__lead, .xd-hero__cta, .xd-stats, .xd-float-card").forEach((el, i) => {
      el.classList.add("xd-fade-in");
      el.style.setProperty("--delay", `${0.9 + i * 0.1}s`);
      setTimeout(() => el.classList.add("is-in"), 80);
    });
  }

  /* ═══ COMPTEURS ═══ */
  function animateCounters() {
    if (reduce) return;
    hero.querySelectorAll("[data-count]").forEach((el) => {
      const target = parseInt(el.dataset.count, 10) || 0;
      const dur = 1800;
      const start = performance.now();
      function tick(now) {
        const t = Math.min((now - start) / dur, 1);
        const ease = 1 - Math.pow(1 - t, 4);
        el.textContent = Math.round(target * ease);
        if (t < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
  }

  /* ═══ AURA CURSEUR HERO ═══ */
  const glow = hero.querySelector(".xd-hero__cursor-glow");
  if (glow && fine && !reduce) {
    hero.addEventListener("mousemove", (e) => {
      const r = hero.getBoundingClientRect();
      const x = e.clientX - r.left;
      const y = e.clientY - r.top;
      glow.style.transform = `translate(${x - 200}px, ${y - 200}px)`;
      glow.style.opacity = "1";
    });
    hero.addEventListener("mouseleave", () => {
      glow.style.opacity = "0";
    });
  }

  /* ═══ PARALLAXE HERO ═══ */
  const visual = hero.querySelector(".xd-hero__visual");
  const copy = hero.querySelector(".xd-hero__copy");
  const watermark = hero.querySelector(".xd-hero__watermark");
  const orbs = hero.querySelectorAll(".xd-orb");

  function onHeroScroll() {
    const y = window.scrollY;
    const p = Math.min(y / window.innerHeight, 1);
    if (visual && !reduce) {
      visual.style.transform = `translateY(${y * 0.22}px) rotateX(${p * 6}deg) scale(${1 - p * 0.05})`;
    }
    if (copy && !reduce) copy.style.transform = `translateY(${y * 0.1}px)`;
    if (watermark && !reduce) watermark.style.transform = `translateY(${y * 0.35}px) scale(${1 + p * 0.08})`;
    orbs.forEach((orb, i) => {
      if (!reduce) orb.style.transform = `translateY(${y * (0.08 + i * 0.04)}px)`;
    });
    hero.style.setProperty("--hero-fade", String(1 - p * 0.4));
  }

  /* ═══ TILT CARTES FLOTTANTES ═══ */
  const cards = hero.querySelectorAll(".xd-float-card");
  if (fine && !reduce && cards.length) {
    hero.addEventListener("mousemove", (e) => {
      const rect = hero.getBoundingClientRect();
      const x = (e.clientX - rect.left) / rect.width - 0.5;
      const y = (e.clientY - rect.top) / rect.height - 0.5;
      cards.forEach((card, i) => {
        const f = 1 + i * 0.35;
        card.style.transform = `translate3d(${x * 18 * f}px, ${y * 14 * f}px, ${i * 20}px) rotateX(${-y * 8}deg) rotateY(${x * 8}deg)`;
      });
    });
    hero.addEventListener("mouseleave", () => {
      cards.forEach((c) => { c.style.transform = ""; });
    });
  }

  /* ═══ SCROLL PIN HORIZONTAL (produits) ═══ */
  function initPinScroll() {
    const section = document.getElementById("xd-pin-products");
    if (!section || reduce) return;
    const track = section.querySelector(".xd-pin-scroll__track");
    const bar = section.querySelector(".xd-pin-scroll__progress span");
    if (!track) return;

    let trackW = 0;
    let scrollLen = 0;

    function measure() {
      const cards = track.children;
      if (!cards.length) return;
      const last = cards[cards.length - 1];
      trackW = last.offsetLeft + last.offsetWidth - track.offsetLeft + 80;
      const viewW = section.querySelector(".xd-pin-scroll__viewport")?.offsetWidth || window.innerWidth;
      scrollLen = Math.max(0, trackW - viewW);
      section.style.height = `${window.innerHeight + scrollLen + 120}px`;
    }

    function update() {
      if (window.innerWidth < 900) {
        track.style.transform = "";
        section.style.height = "";
        return;
      }
      const rect = section.getBoundingClientRect();
      const total = section.offsetHeight - window.innerHeight;
      if (total <= 0) return;
      const scrolled = Math.min(Math.max(-rect.top, 0), total);
      const p = scrolled / total;
      track.style.transform = `translate3d(${-p * scrollLen}px, 0, 0)`;
      if (bar) bar.style.width = `${p * 100}%`;
    }

    measure();
    window.addEventListener("resize", () => { measure(); update(); });
    window.addEventListener("scroll", () => { update(); onHeroScroll(); }, { passive: true });
    update();
  }

  /* ═══ REVEAL SECTIONS ═══ */
  const reveals = document.querySelectorAll(".xd-reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            e.target.classList.add("is-visible");
            io.unobserve(e.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -6% 0px" }
    );
    reveals.forEach((el) => io.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  /* ═══ STAGGER BENTO ═══ */
  const bento = document.querySelector(".xd-bento");
  if (bento) {
    bento.querySelectorAll(".xd-bento__cell").forEach((cell, i) => {
      cell.style.setProperty("--stagger", `${i * 0.08}s`);
      cell.classList.add("xd-stagger");
    });
    if ("IntersectionObserver" in window) {
      const bio = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting) {
            bento.classList.add("is-visible");
            bio.disconnect();
          }
        },
        { threshold: 0.15 }
      );
      bio.observe(bento);
    } else {
      bento.classList.add("is-visible");
    }
  }

  /* ═══ MAGNÉTISME BOUTONS ═══ */
  if (fine && !reduce) {
    document.querySelectorAll(".xd-magnetic").forEach((btn) => {
      btn.addEventListener("mousemove", (e) => {
        const r = btn.getBoundingClientRect();
        btn.style.transform = `translate(${(e.clientX - r.left - r.width / 2) * 0.2}px, ${(e.clientY - r.top - r.height / 2) * 0.25}px)`;
      });
      btn.addEventListener("mouseleave", () => { btn.style.transform = ""; });
    });
  }

  /* ═══ TILT PRODUITS ═══ */
  if (fine && !reduce) {
    document.querySelectorAll(".xd-product--premium").forEach((card) => {
      card.addEventListener("mousemove", (e) => {
        const r = card.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(800px) rotateX(${-y * 8}deg) rotateY(${x * 8}deg) translateY(-8px)`;
        const shine = card.querySelector(".xd-product__shine");
        if (shine) {
          shine.style.background = `radial-gradient(circle at ${(x + 0.5) * 100}% ${(y + 0.5) * 100}%, rgba(255,255,255,0.18), transparent 55%)`;
        }
      });
      card.addEventListener("mouseleave", () => {
        card.style.transform = "";
        const shine = card.querySelector(".xd-product__shine");
        if (shine) shine.style.background = "";
      });
    });
  }

  /* ═══ PARTICULES FINALE ═══ */
  const finaleParticles = document.querySelector(".xd-finale__particles");
  if (finaleParticles && !reduce) {
    for (let i = 0; i < 24; i++) {
      const p = document.createElement("span");
      p.style.cssText = [
        `--x:${Math.random() * 100}%`,
        `--y:${Math.random() * 100}%`,
        `--d:${2 + Math.random() * 4}s`,
        `--delay:${Math.random() * 3}s`,
      ].join(";");
      finaleParticles.appendChild(p);
    }
  }

  /* ═══ NUMÉROS SECTION PARALLAXE ═══ */
  document.querySelectorAll("[data-parallax-num]").forEach((num) => {
    if (reduce) return;
    window.addEventListener(
      "scroll",
      () => {
        const rect = num.getBoundingClientRect();
        const offset = (rect.top - window.innerHeight * 0.5) * 0.08;
        num.style.transform = `translateY(${offset}px)`;
      },
      { passive: true }
    );
  });

  /* ═══ INIT ═══ */
  splitLines();
  runPreloader(() => {
    revealHero();
    animateCounters();
    if (document.getElementById("xd-pin-products")) {
      initPinScroll();
    } else {
      window.addEventListener("scroll", onHeroScroll, { passive: true });
    }
    onHeroScroll();
  });
})();
