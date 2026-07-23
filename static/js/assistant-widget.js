(function () {
  var root = document.getElementById("assistant-widget");
  if (!root) return;

  var fab = document.getElementById("assistant-fab");
  var panel = document.getElementById("assistant-panel");
  var closeBtn = document.getElementById("assistant-close");
  var form = document.getElementById("assistant-form");
  var input = document.getElementById("assistant-input");
  var messages = document.getElementById("assistant-messages");
  var chips = document.getElementById("assistant-chips");
  var busy = false;
  var askedOnce = false;

  var WELCOME =
    "Bonjour, je suis le conseiller Yombal Market.\n\n" +
    "Je peux vous renseigner sur la boutique (épicerie, smartphones, " +
    "électroménager, habillement, chaussures, sacs, commandes, livraisons) " +
    "et sur l'ensemble des services du Groupe YOMBAL : Voyages, Investissement, " +
    "Immobilier & BTP, Transports, Restaurant, Électronique, Électroménager, " +
    "Habillement, Chaussures, Sacs & bagagerie et Coiffure.\n\n" +
    "Écrivez-moi dans votre langue : français, anglais, wolof, espagnol, " +
    "portugais, allemand, italien, arabe…";

  var SUGGESTIONS = [
    { label: "Services du Groupe", q: "Quels sont les services du Groupe YOMBAL ?" },
    { label: "Smartphones", q: "Avez-vous des iPhone ou Samsung ?" },
    { label: "Électroménager", q: "Je cherche un mixeur ou une friteuse" },
    { label: "Habillement", q: "Avez-vous des vêtements ou un boubou ?" },
    { label: "Immobilier & BTP", q: "Je cherche un terrain au Sénégal" },
    { label: "Suivi commande", q: "Comment suivre ma commande ?" },
  ];

  function adjustForCookieBanner() {
    var banner = document.getElementById("cookie-consent");
    if (!banner || banner.hidden) {
      document.body.classList.remove("cookie-banner-visible");
      return;
    }
    document.body.classList.add("cookie-banner-visible");
  }

  function renderChips() {
    if (!chips || chips.dataset.ready === "1") return;
    chips.innerHTML = "";
    var label = document.createElement("p");
    label.className = "assistant-chips-label";
    label.textContent = "Questions fréquentes";
    chips.appendChild(label);
    SUGGESTIONS.forEach(function (item) {
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "assistant-chip";
      btn.textContent = item.label;
      btn.addEventListener("click", function () {
        if (busy) return;
        sendQuestion(item.q);
      });
      chips.appendChild(btn);
    });
    chips.dataset.ready = "1";
    chips.hidden = false;
  }

  function hideChips() {
    if (chips) chips.hidden = true;
  }

  function setOpen(open) {
    if (!fab || !panel) return;
    fab.setAttribute("aria-expanded", open ? "true" : "false");
    panel.classList.toggle("is-open", open);
    panel.setAttribute("aria-hidden", open ? "false" : "true");
    if (open) {
      if (!messages || !messages.children.length) {
        addBotMessage(WELCOME);
        renderChips();
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
      ecosystem: "Service",
    };
    return labels[src.type] || "Lien";
  }

  function renderSources(sources) {
    if (!sources || !sources.length) return "";
    var links = sources
      .map(function (src, index) {
        if (!src.url) return "";
        var title = escapeHtml(src.title || src.id || "Consulter");
        var cls = index === 0 ? "" : " is-secondary";
        var target =
          src.url.indexOf("http") === 0
            ? ' target="_blank" rel="noopener noreferrer"'
            : "";
        return (
          '<a class="' +
          cls.trim() +
          '" href="' +
          escapeHtml(src.url) +
          '"' +
          target +
          ">" +
          sourceLabel(src) +
          " — " +
          title +
          "</a>"
        );
      })
      .filter(Boolean)
      .join("");
    if (!links) return "";
    return '<div class="assistant-sources"><strong>Accès rapide</strong>' + links + "</div>";
  }

  function renderCtaLinks(sources) {
    if (!sources || !sources.length) return "";
    var html = '<div class="assistant-cta">';
    sources.forEach(function (src, index) {
      if (!src.url) return;
      var cls = index === 0 ? "" : " is-secondary";
      var target =
        src.url.indexOf("http") === 0
          ? ' target="_blank" rel="noopener noreferrer"'
          : "";
      html +=
        '<a class="' +
        cls.trim() +
        '" href="' +
        escapeHtml(src.url) +
        '"' +
        target +
        ">" +
        escapeHtml(src.title || "Consulter") +
        "</a>";
    });
    html += "</div>";
    return html;
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
    if (chips) {
      chips.querySelectorAll(".assistant-chip").forEach(function (chip) {
        chip.disabled = state;
      });
    }
  }

  function sendQuestion(question) {
    if (!question || busy) return;
    if (!askedOnce) {
      askedOnce = true;
      hideChips();
    }
    addUserMessage(question);
    var loadingEl = addMessage("bot", "Recherche en cours…", "assistant-msg--loading");
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
        var answer = data.answer || "Réponse indisponible pour le moment. Merci de réessayer.";
        if (data.hint === "order_tracking") {
          addMessage(
            "bot",
            formatBotHtml(answer) +
              '<div class="assistant-cta"><a href="/suivi-commande">Accéder au suivi de commande</a></div>'
          );
        } else if (data.hint === "ecosystem") {
          addMessage("bot", formatBotHtml(answer) + renderCtaLinks(data.sources || []));
        } else {
          addBotMessage(answer, data.sources);
        }
      })
      .catch(function () {
        if (loadingEl && loadingEl.parentNode) loadingEl.parentNode.removeChild(loadingEl);
        addBotMessage(
          "La connexion au conseiller a échoué. Veuillez réessayer dans un instant, ou utilisez la page Contact."
        );
      })
      .finally(function () {
        setBusy(false);
        if (input) input.focus();
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
