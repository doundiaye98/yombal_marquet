/**
 * PWA install — iPhone/Safari = guide manuel (pas d'API native).
 * Chromium = beforeinstallprompt quand dispo.
 */
(function () {
  "use strict";

  function $(id) {
    return document.getElementById(id);
  }

  var btn = $("pwa-install-btn");
  var btnMobile = $("pwa-install-btn-mobile");
  var sheet = $("pwa-ios-hint");
  var sheetClose = $("pwa-ios-close");
  var sheetText = $("pwa-ios-text");
  var deferredPrompt = null;

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

  function isIos() {
    var ua = window.navigator.userAgent || "";
    return /iPhone|iPad|iPod/i.test(ua) ||
      (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  }

  function isAndroid() {
    return /Android/i.test(window.navigator.userAgent || "");
  }

  function showEl(el) {
    if (!el) return;
    el.hidden = false;
    el.removeAttribute("hidden");
    el.classList.add("is-visible");
    el.setAttribute("aria-hidden", "false");
  }

  function hideEl(el) {
    if (!el) return;
    el.hidden = true;
    el.setAttribute("hidden", "hidden");
    el.classList.remove("is-visible");
    el.setAttribute("aria-hidden", "true");
  }

  function showButtons() {
    showEl(btn);
    showEl(btnMobile);
  }

  function hideButtons() {
    hideEl(btn);
    hideEl(btnMobile);
  }

  function openGuide() {
    if (!sheet) {
      window.alert(
        isIos()
          ? "Pour installer : Partager → Sur l'écran d'accueil"
          : "Pour installer : menu du navigateur → Ajouter à l'écran d'accueil"
      );
      return;
    }
    if (sheetText) {
      if (isIos()) {
        sheetText.innerHTML =
          "1. Appuyez sur le bouton <strong>Partager</strong> <span aria-hidden=\"true\">□↑</span> en bas de Safari.<br>" +
          "2. Faites défiler et choisissez <strong>« Sur l'écran d'accueil »</strong>.<br>" +
          "3. Validez avec <strong>Ajouter</strong>.";
      } else if (isAndroid()) {
        sheetText.innerHTML =
          "Ouvrez le menu <strong>⋮</strong> puis <strong>« Installer l'application »</strong> " +
          "ou <strong>« Ajouter à l'écran d'accueil »</strong>.";
      } else {
        sheetText.innerHTML =
          "Menu du navigateur → <strong>Installer l'application</strong> " +
          "ou <strong>Ajouter à l'écran d'accueil</strong>.";
      }
    }
    showEl(sheet);
    sheet.setAttribute("role", "dialog");
  }

  function closeGuide() {
    hideEl(sheet);
  }

  function onInstallTap(event) {
    if (event) {
      event.preventDefault();
      event.stopPropagation();
    }

    // Feedback visuel immédiat (iOS)
    var target = (event && event.currentTarget) || btn;
    if (target && target.classList) {
      target.classList.add("is-pressed");
      window.setTimeout(function () {
        target.classList.remove("is-pressed");
      }, 180);
    }

    if (deferredPrompt) {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then(function () {
        deferredPrompt = null;
        hideButtons();
        closeGuide();
      }).catch(function () {
        openGuide();
      });
      return;
    }

    // iPhone / Safari / pas d'API → guide
    openGuide();
  }

  // Exposé pour onclick HTML (filet de sécurité iOS)
  window.yombalInstallPwa = onInstallTap;

  if (isStandalone()) {
    hideButtons();
    closeGuide();
    return;
  }

  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js", { scope: "/" }).catch(function () {});
  }

  window.addEventListener("beforeinstallprompt", function (event) {
    event.preventDefault();
    deferredPrompt = event;
    showButtons();
  });

  window.addEventListener("appinstalled", function () {
    deferredPrompt = null;
    hideButtons();
    closeGuide();
  });

  function bind(el) {
    if (!el) return;
    el.addEventListener("click", onInstallTap, false);
  }

  bind(btn);
  bind(btnMobile);

  if (sheetClose) {
    sheetClose.addEventListener("click", function (e) {
      e.preventDefault();
      closeGuide();
    }, false);
  }

  if (sheet) {
    sheet.addEventListener("click", function (e) {
      if (e.target === sheet) closeGuide();
    }, false);
  }

  // Toujours visible hors mode app installée
  showButtons();
})();
