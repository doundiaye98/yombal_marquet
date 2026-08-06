/**
 * PWA — iPhone : le guide s'ouvre en CSS via #pwa-install-sheet (sans JS).
 * Chromium : si beforeinstallprompt est dispo, on utilise le prompt natif.
 */
(function () {
  "use strict";

  var deferredPrompt = null;
  var btn = document.getElementById("pwa-install-btn");
  var btnMobile = document.getElementById("pwa-install-btn-mobile");

  function isStandalone() {
    try {
      return (
        window.matchMedia("(display-mode: standalone)").matches ||
        window.navigator.standalone === true
      );
    } catch (e) {
      return false;
    }
  }

  function hideInstallUi() {
    if (btn) btn.style.display = "none";
    if (btnMobile) btnMobile.style.display = "none";
    if (window.location.hash === "#pwa-install-sheet") {
      window.location.hash = "";
    }
  }

  if (isStandalone()) {
    hideInstallUi();
    return;
  }

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
  }

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferredPrompt = event;
  });

  window.addEventListener("appinstalled", function () {
    deferredPrompt = null;
    hideInstallUi();
  });

  function onChromeInstall(event) {
    if (!deferredPrompt) return; // laisse le lien # ouvrir le guide
    event.preventDefault();
    deferredPrompt.prompt();
    deferredPrompt.userChoice.finally(function () {
      deferredPrompt = null;
    });
  }

  if (btn) btn.addEventListener("click", onChromeInstall);
  if (btnMobile) btnMobile.addEventListener("click", onChromeInstall);
})();
