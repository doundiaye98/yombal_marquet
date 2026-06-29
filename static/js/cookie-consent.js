(function () {
  var KEY = "yombal_cookie_consent";
  var banner = document.getElementById("cookie-consent");
  if (!banner) return;
  try {
    if (localStorage.getItem(KEY) === "1") return;
  } catch (e) {
    /* ignore */
  }
  banner.hidden = false;
  banner.setAttribute("aria-hidden", "false");

  function accept() {
    try {
      localStorage.setItem(KEY, "1");
    } catch (e) {
      /* ignore */
    }
    banner.hidden = true;
    banner.setAttribute("aria-hidden", "true");
  }

  var btn = banner.querySelector("[data-cookie-accept]");
  if (btn) btn.addEventListener("click", accept);
})();
