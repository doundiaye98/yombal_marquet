/**
 * Accueil marketplace — bandeau + carrousels horizontaux
 */
(function () {
  const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  const banner = document.querySelector(".mp-banner");
  if (banner) {
    const slides = banner.querySelectorAll(".mp-banner__slide");
    const dots = banner.querySelectorAll(".mp-banner__dot");
    let index = 0;
    let timer;

    function show(i) {
      index = (i + slides.length) % slides.length;
      slides.forEach((s, j) => s.classList.toggle("is-active", j === index));
      dots.forEach((d, j) => d.classList.toggle("is-active", j === index));
    }

    dots.forEach((dot, i) => {
      dot.addEventListener("click", () => {
        show(i);
        resetTimer();
      });
    });

    function resetTimer() {
      clearInterval(timer);
      if (!reduce && slides.length > 1) {
        timer = setInterval(() => show(index + 1), 6000);
      }
    }

    if (slides.length) {
      show(0);
      resetTimer();
    }
  }

  document.querySelectorAll("[data-mp-scroll]").forEach((wrap) => {
    const track = wrap.querySelector(".mp-scroll__track");
    const prev = wrap.querySelector(".mp-scroll__btn--prev");
    const next = wrap.querySelector(".mp-scroll__btn--next");
    if (!track) return;

    const step = () => Math.max(track.clientWidth * 0.75, 200);

    prev?.addEventListener("click", () => {
      track.scrollBy({ left: -step(), behavior: "smooth" });
    });
    next?.addEventListener("click", () => {
      track.scrollBy({ left: step(), behavior: "smooth" });
    });
  });
})();
