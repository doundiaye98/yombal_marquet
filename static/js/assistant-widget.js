(function () {
  var root = document.getElementById("assistant-widget");
  if (!root) return;

  var fab = document.getElementById("assistant-fab");
  var panel = document.getElementById("assistant-panel");
  var closeBtn = document.getElementById("assistant-close");
  var form = document.getElementById("assistant-form");
  var input = document.getElementById("assistant-input");
  var messages = document.getElementById("assistant-messages");
  var busy = false;

  var WELCOME =
    "Bonjour ! Je suis l'assistant Yombal Marché. " +
    "Posez-moi une question sur nos produits, recettes, coffrets ou modes de paiement.";

  function adjustForCookieBanner() {
    var banner = document.getElementById("cookie-consent");
    if (!banner || banner.hidden) {
      document.body.classList.remove("cookie-banner-visible");
      return;
    }
    document.body.classList.add("cookie-banner-visible");
  }

  function setOpen(open) {
    if (!fab || !panel) return;
    fab.setAttribute("aria-expanded", open ? "true" : "false");
    panel.classList.toggle("is-open", open);
    panel.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) {
      if (!messages || !messages.children.length) {
        addBotMessage(WELCOME);
      }
      setTimeout(function () {
        if (input) input.focus();
      }, 120);
    }
  }

  function scrollMessages() {
    if (!messages) return;
    messages.scrollTop = messages.scrollHeight;
  }

  function escapeHtml(text) {
    return String(text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function formatBotHtml(text) {
    return escapeHtml(text).replace(/\n/g, "<br>");
  }

  function sourceLabel(src) {
    var labels = {
      product: "Produit",
      recipe: "Recette",
      coffret: "Coffret",
      faq: "FAQ",
      producer: "Producteur",
    };
    return labels[src.type] || "Voir";
  }

  function renderSources(sources) {
    if (!sources || !sources.length) return "";
    var links = sources
      .map(function (src) {
        if (!src.url) return "";
        var title = escapeHtml(src.title || src.id || "Lien");
        return '<a href="' + escapeHtml(src.url) + '">' + sourceLabel(src) + " : " + title + "</a>";
      })
      .filter(Boolean)
      .join("");
    if (!links) return "";
    return '<div class="assistant-sources"><strong>Sources</strong>' + links + "</div>";
  }

  function addMessage(role, html, extraClass) {
    if (!messages) return null;
    var el = document.createElement("div");
    el.className = "assistant-msg assistant-msg--" + role + (extraClass ? " " + extraClass : "");
    el.innerHTML = html;
    messages.appendChild(el);
    scrollMessages();
    return el;
  }

  function addUserMessage(text) {
    addMessage("user", escapeHtml(text));
  }

  function addBotMessage(text, sources) {
    addMessage("bot", formatBotHtml(text) + renderSources(sources));
  }

  function setBusy(state) {
    busy = state;
    if (input) input.disabled = state;
    if (form) {
      var btn = form.querySelector(".assistant-send");
      if (btn) btn.disabled = state;
    }
  }

  function sendQuestion(question) {
    if (!question || busy) return;
    addUserMessage(question);
    var loadingEl = addMessage("bot", "Je réfléchis…", "assistant-msg--loading");
    setBusy(true);

    fetch("/api/assistant", {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify({ question: question }),
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, status: res.status, data: data };
        });
      })
      .then(function (result) {
        if (loadingEl && loadingEl.parentNode) loadingEl.parentNode.removeChild(loadingEl);
        var data = result.data || {};
        var answer = data.answer || "Réponse indisponible pour le moment.";
        if (data.hint === "order_tracking") {
          addMessage(
            "bot",
            formatBotHtml(answer) +
              '<p style="margin-top:10px"><a href="/suivi-commande">→ Ouvrir le suivi de commande</a></p>'
          );
        } else {
          addBotMessage(answer, data.sources);
        }
      })
      .catch(function () {
        if (loadingEl && loadingEl.parentNode) loadingEl.parentNode.removeChild(loadingEl);
        addBotMessage(
          "Connexion impossible. Réessayez dans un instant ou contactez-nous via la page Contact."
        );
      })
      .finally(function () {
        setBusy(false);
        if (input) {
          input.focus();
        }
      });
  }

  if (fab) {
    fab.addEventListener("click", function () {
      var open = fab.getAttribute("aria-expanded") === "true";
      setOpen(!open);
    });
  }

  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      setOpen(false);
      if (fab) fab.focus();
    });
  }

  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!input) return;
      var question = (input.value || "").trim();
      if (!question) return;
      input.value = "";
      sendQuestion(question);
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && panel && panel.classList.contains("is-open")) {
      setOpen(false);
      if (fab) fab.focus();
    }
  });

  adjustForCookieBanner();
  var cookieBtn = document.querySelector("[data-cookie-accept]");
  if (cookieBtn) {
    cookieBtn.addEventListener("click", function () {
      setTimeout(adjustForCookieBanner, 50);
    });
  }
})();
