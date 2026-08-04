/**
 * Bouton d'installation PWA — desktop + mobile.
 * - Chromium : beforeinstallprompt → prompt natif
 * - iOS / fallback : guide d'installation
 */
(function () {
  const btn = document.getElementById("pwa-install-btn");
  const btnMobile = document.getElementById("pwa-install-btn-mobile");
  const iosHint = document.getElementById("pwa-ios-hint");
  const iosClose = document.getElementById("pwa-ios-close");
  const iosText = document.getElementById("pwa-ios-text");
  if (!btn && !btnMobile) return;

  let deferredPrompt = null;

  function isStandalone() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.navigator.standalone === true
    );
  }

  function isIos() {
    return /iphone|ipad|ipod/i.test(window.navigator.userAgent) ||
      (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  }

  function isAndroid() {
    return /android/i.test(window.navigator.userAgent);
  }

  function show(el) {
    if (!el) return;
    el.hidden = false;
    el.removeAttribute("hidden");
    el.setAttribute("aria-hidden", "false");
  }

  function hide(el) {
    if (!el) return;
    el.hidden = true;
    el.setAttribute("hidden", "");
    el.setAttribute("aria-hidden", "true");
  }

  function setButtonsVisible(visible) {
    if (visible) {
      show(btn);
      show(btnMobile);
    } else {
      hide(btn);
      hide(btnMobile);
    }
  }

  function showHelp() {
    if (!iosHint) return;
    if (iosText) {
      if (isIos()) {
        iosText.innerHTML =
          "Sur iPhone / iPad : appuyez sur <strong>Partager</strong> " +
          "puis <strong>« Sur l'écran d'accueil »</strong>.";
      } else if (isAndroid()) {
        iosText.innerHTML =
          "Sur Android : ouvrez le menu <strong>⋮</strong> du navigateur " +
          "puis choisissez <strong>« Installer l'application »</strong> " +
          "ou <strong>« Ajouter à l'écran d'accueil »</strong>.";
      } else {
        iosText.innerHTML =
          "Dans votre navigateur, ouvrez le menu puis choisissez " +
          "<strong>« Installer l'application »</strong> " +
          "ou <strong>« Ajouter à l'écran d'accueil »</strong>.";
      }
    }
    show(iosHint);
  }

  async function triggerInstall(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }

    if (deferredPrompt) {
      try {
        deferredPrompt.prompt();
        await deferredPrompt.userChoice;
      } catch (_err) {
        showHelp();
      }
      deferredPrompt = null;
      setButtonsVisible(false);
      hide(iosHint);
      return;
    }

    showHelp();
  }

  if (isStandalone()) {
    setButtonsVisible(false);
    hide(iosHint);
    return;
  }

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
  }

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferredPrompt = event;
    setButtonsVisible(true);
  });

  window.addEventListener("appinstalled", function () {
    deferredPrompt = null;
    setButtonsVisible(false);
    hide(iosHint);
  });

  if (btn) {
    btn.addEventListener("click", triggerInstall);
  }

  if (btnMobile) {
    btnMobile.addEventListener("click", triggerInstall);
  }

  if (iosClose && iosHint) {
    iosClose.addEventListener("click", function () {
      hide(iosHint);
    });
  }

  // Afficher le bouton tout de suite sur mobile (guide si pas encore installable)
  if (isIos() || isAndroid() || window.matchMedia("(max-width: 900px)").matches) {
    setButtonsVisible(true);
  }
})();
