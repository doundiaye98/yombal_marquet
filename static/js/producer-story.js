(function () {
  "use strict";

  if (!("speechSynthesis" in window)) return;

  let activeBtn = null;
  let utterance = null;

  function pickFrenchVoice() {
    const voices = window.speechSynthesis.getVoices();
    return (
      voices.find((v) => v.lang && v.lang.toLowerCase().startsWith("fr")) ||
      voices[0] ||
      null
    );
  }

  function resetButton(btn) {
    if (!btn) return;
    btn.classList.remove("is-playing");
    btn.setAttribute("aria-pressed", "false");
    const label = btn.querySelector(".story-audio-label");
    if (label) label.textContent = "Écouter l'histoire";
  }

  function stopCurrent() {
    window.speechSynthesis.cancel();
    if (activeBtn) {
      resetButton(activeBtn);
      activeBtn = null;
    }
    utterance = null;
  }

  function startPlayback(btn, text) {
    stopCurrent();

    const clean = (text || "").trim();
    if (!clean) return;

    const excerpt =
      clean.length > 520 ? clean.slice(0, 520).trim() + "…" : clean;

    utterance = new SpeechSynthesisUtterance(excerpt);
    utterance.lang = "fr-FR";
    utterance.rate = 0.92;
    utterance.pitch = 1;

    const voice = pickFrenchVoice();
    if (voice) utterance.voice = voice;

    utterance.onend = stopCurrent;
    utterance.onerror = stopCurrent;

    activeBtn = btn;
    btn.classList.add("is-playing");
    btn.setAttribute("aria-pressed", "true");
    const label = btn.querySelector(".story-audio-label");
    if (label) label.textContent = "Arrêter la lecture";

    window.speechSynthesis.speak(utterance);
  }

  document.querySelectorAll(".story-audio").forEach((wrap) => {
    const btn = wrap.querySelector(".story-audio-btn");
    if (!btn) return;

    btn.addEventListener("click", () => {
      if (btn.classList.contains("is-playing")) {
        stopCurrent();
        return;
      }
      const text = wrap.getAttribute("data-story") || "";
      startPlayback(btn, text);
    });
  });

  window.speechSynthesis.onvoiceschanged = function () {
    pickFrenchVoice();
  };
})();
