/**
 * Bouton d'installation PWA + enregistrement du service worker.
 * Affiche le bouton seulement si l'app est installable (Chromium)
 * ou propose un guide iOS (Safari).
 */
(function () {
  const btn = document.getElementById("pwa-install-btn");
  const iosHint = document.getElementById("pwa-ios-hint");
  const iosClose = document.getElementById("pwa-ios-close");
  if (!btn) return;

  let deferredPrompt = null;

  function isStandalone() {
    return (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.navigator.standalone === true
    );
  }

  function isIos() {
    return /iphone|ipad|ipod/i.test(window.navigator.userAgent);
  }

  function show(el) {
    if (el) el.hidden = false;
  }

  function hide(el) {
    if (el) el.hidden = true;
  }

  function syncMobileBtn(visible) {
    const mobile = document.getElementById("pwa-install-btn-mobile");
    if (!mobile) return;
    mobile.hidden = !visible;
  }

  if (isStandalone()) {
    hide(btn);
    hide(iosHint);
    syncMobileBtn(false);
    return;
  }

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {
      /* silencieux : PWA optionnelle */
    });
  }

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferredPrompt = event;
    show(btn);
    btn.setAttribute("aria-hidden", "false");
    syncMobileBtn(true);
  });

  window.addEventListener("appinstalled", function () {
    deferredPrompt = null;
    hide(btn);
    hide(iosHint);
    syncMobileBtn(false);
  });

  btn.addEventListener("click", async function () {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      try {
        await deferredPrompt.userChoice;
      } catch (_err) {
        /* ignore */
      }
      deferredPrompt = null;
      hide(btn);
      syncMobileBtn(false);
      return;
    }
    if (isIos() && iosHint) {
      show(iosHint);
    }
  });

  if (iosClose && iosHint) {
    iosClose.addEventListener("click", function () {
      hide(iosHint);
    });
  }

  // Sur iOS Safari : proposer le bouton (pas de beforeinstallprompt)
  if (isIos() && !isStandalone()) {
    show(btn);
    btn.setAttribute("aria-hidden", "false");
    syncMobileBtn(true);
  }
})();
