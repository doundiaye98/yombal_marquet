/**
 * Alertes navigateur pour le suivi de commande (Notification API + polling léger).
 */
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("order-push-enable");
  if (!btn) return;

  const orderId = btn.dataset.orderId;
  const statusUrl = btn.dataset.statusUrl;
  const statusEl = document.getElementById("order-push-status");
  const storageKey = `yombal_order_watch_${orderId}`;

  function setHint(text, visible = true) {
    if (!statusEl) return;
    statusEl.textContent = text;
    statusEl.hidden = !visible;
  }

  function showNotification(title, body) {
    if (!("Notification" in window) || Notification.permission !== "granted") return;
    try {
      new Notification(title, {
        body,
        icon: "/static/images/favicon.ico",
        tag: `yombal-order-${orderId}`,
      });
    } catch {
      /* ignore */
    }
  }

  async function pollStatus() {
    if (!statusUrl || Notification.permission !== "granted") return;
    if (localStorage.getItem(storageKey) !== "1") return;
    try {
      const res = await fetch(statusUrl, { credentials: "same-origin" });
      if (!res.ok) return;
      const data = await res.json();
      const prev = btn.dataset.orderStatus;
      if (data.status && data.status !== prev) {
        btn.dataset.orderStatus = data.status;
        showNotification(
          "Yombal Marché — commande mise à jour",
          data.status_label || "Statut modifié"
        );
        setHint(`Dernière alerte : ${data.status_label}`, true);
      }
    } catch {
      /* ignore network errors */
    }
  }

  btn.addEventListener("click", async () => {
    if (!("Notification" in window)) {
      setHint("Votre navigateur ne supporte pas les notifications.", true);
      return;
    }
    let perm = Notification.permission;
    if (perm === "default") {
      perm = await Notification.requestPermission();
    }
    if (perm !== "granted") {
      setHint("Autorisez les notifications dans les paramètres du navigateur.", true);
      return;
    }
    localStorage.setItem(storageKey, "1");
    btn.textContent = "✓ Alertes navigateur activées";
    btn.disabled = true;
    setHint("Vous serez prévenu si le statut change (même onglet fermé).", true);
    showNotification("Yombal Marché", "Suivi de commande activé.");
    pollStatus();
  });

  if (localStorage.getItem(storageKey) === "1" && Notification.permission === "granted") {
    btn.textContent = "✓ Alertes navigateur activées";
    btn.disabled = true;
    setHint("Surveillance active — e-mail/SMS également envoyés si activés.", true);
    window.setInterval(pollStatus, 60000);
  }
});
