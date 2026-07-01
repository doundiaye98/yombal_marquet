(function () {
  "use strict";

  var root = document.querySelector("[data-gamme-filters]");
  if (!root) return;

  var cards = Array.prototype.slice.call(document.querySelectorAll("[data-gamme-card]"));
  var countEl = document.querySelector("[data-gamme-count]");
  var emptyEl = document.querySelector("[data-gamme-empty]");
  var state = { type: "", format: "" };

  function setActivePill(kind, value) {
    var pills = root.querySelectorAll('[data-filter-kind="' + kind + '"]');
    pills.forEach(function (pill) {
      var match = (pill.getAttribute("data-filter-value") || "") === value;
      pill.classList.toggle("is-active", match);
    });
  }

  function applyFilters() {
    var visible = 0;
    cards.forEach(function (card) {
      var okType = !state.type || card.getAttribute("data-type") === state.type;
      var okFormat = !state.format || card.getAttribute("data-format") === state.format;
      var show = okType && okFormat;
      card.hidden = !show;
      card.classList.toggle("is-filtered-out", !show);
      if (show) visible += 1;
    });
    if (countEl) {
      countEl.textContent =
        visible +
        " référence" +
        (visible > 1 ? "s" : "") +
        (state.type || state.format ? " (filtré)" : "");
    }
    if (emptyEl) {
      emptyEl.classList.toggle("is-hidden", visible > 0);
    }
  }

  function readUrl() {
    var params = new URLSearchParams(window.location.search);
    state.type = params.get("type") || "";
    state.format = params.get("format") || "";
    setActivePill("type", state.type);
    setActivePill("format", state.format);
    applyFilters();
  }

  function writeUrl() {
    var params = new URLSearchParams();
    if (state.type) params.set("type", state.type);
    if (state.format) params.set("format", state.format);
    var qs = params.toString();
    var next = window.location.pathname + (qs ? "?" + qs : "");
    window.history.replaceState({}, "", next);
  }

  root.addEventListener("click", function (event) {
    var pill = event.target.closest("[data-filter-kind]");
    if (!pill) return;
    var kind = pill.getAttribute("data-filter-kind");
    var value = pill.getAttribute("data-filter-value") || "";
    state[kind] = value;
    setActivePill(kind, value);
    applyFilters();
    writeUrl();
  });

  readUrl();
})();
