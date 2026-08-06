<section class="section-block">
  <div class="section-head">
    <h1>Paiement</h1>
    <p>Commande <strong><?= e($order['public_ref']) ?></strong> — <?= e(money_eur((int) $order['total_cents'])) ?></p>
  </div>

  <ul>
    <?php foreach ($items as $it): ?>
    <li><?= e($it['product_name']) ?> × <?= (int) $it['quantity'] ?> — <?= e(money_eur((int) $it['line_total_cents'])) ?></li>
    <?php endforeach; ?>
  </ul>

  <?php if ($order['status'] !== 'pending'): ?>
  <p>Statut actuel : <strong><?= e(order_status_label($order['status'])) ?></strong></p>
  <a class="xd-btn" href="<?= e(url('/suivi-commande/' . $order['id'])) ?>">Voir le suivi</a>
  <?php else: ?>

  <div style="display:grid;gap:1.25rem;margin-top:2rem;max-width:560px">
    <form method="post" action="<?= e(url('/paiement/' . $order['id'] . '/manuel')) ?>">
      <?= csrf_field() ?>
      <input type="hidden" name="payment_method" value="wire">
      <button type="submit" class="xd-btn" style="width:100%">Virement bancaire</button>
    </form>
    <?php if ($bank['iban']): ?>
    <p class="muted">IBAN : <?= e($bank['iban']) ?> — BIC : <?= e($bank['bic']) ?> — <?= e($bank['holder']) ?> (<?= e($bank['name']) ?>). Indiquez la référence <?= e($order['public_ref']) ?>.</p>
    <?php endif; ?>

    <form method="post" action="<?= e(url('/paiement/' . $order['id'] . '/manuel')) ?>">
      <?= csrf_field() ?>
      <input type="hidden" name="payment_method" value="paypal">
      <button type="submit" class="xd-btn xd-btn--ghost" style="width:100%">PayPal</button>
    </form>
    <?php if ($paypal_email || $paypal_me): ?>
    <p class="muted"><?= e($paypal_email ?: $paypal_me) ?></p>
    <?php endif; ?>

    <form method="post" action="<?= e(url('/paiement/' . $order['id'] . '/manuel')) ?>">
      <?= csrf_field() ?>
      <input type="hidden" name="payment_method" value="cash_delivery">
      <button type="submit" class="xd-btn xd-btn--ghost" style="width:100%">Paiement à la livraison</button>
    </form>

    <?php if ($payment_simulation): ?>
    <form method="post" action="<?= e(url('/paiement/demo/' . $order['id'])) ?>">
      <?= csrf_field() ?>
      <button type="submit" class="xd-btn xd-btn--ghost" style="width:100%">Simuler un paiement (dev)</button>
    </form>
    <?php endif; ?>

    <?php if ($stripe_ok): ?>
    <p class="muted">Stripe est configuré côté serveur — intégration PaymentIntent à activer avec le SDK Stripe PHP sur Hostinger si besoin carte bancaire.</p>
    <?php endif; ?>
  </div>
  <?php endif; ?>
</section>
