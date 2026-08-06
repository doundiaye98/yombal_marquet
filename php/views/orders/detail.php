<section class="section-block">
  <div class="section-head">
    <h1>Commande <?= e($order['public_ref']) ?></h1>
    <?php if (!empty($confirmed)): ?><p class="flash flash-success">Enregistrement confirmé.</p><?php endif; ?>
    <p><strong><?= e(order_status_label($order['status'])) ?></strong> — <?= e(money_eur((int) $order['total_cents'])) ?></p>
  </div>

  <h2>Articles</h2>
  <ul>
    <?php foreach ($items as $it): ?>
    <li><?= e($it['product_name']) ?> × <?= (int) $it['quantity'] ?> — <?= e(money_eur((int) $it['line_total_cents'])) ?></li>
    <?php endforeach; ?>
  </ul>

  <h2>Livraison</h2>
  <p>
    <?= e($order['delivery_line1']) ?><br>
    <?php if ($order['delivery_line2']): ?><?= e($order['delivery_line2']) ?><br><?php endif; ?>
    <?= e($order['delivery_postal_code'] . ' ' . $order['delivery_city']) ?> (<?= e($order['delivery_country']) ?>)
  </p>

  <?php if ($events): ?>
  <h2>Historique</h2>
  <ul>
    <?php foreach ($events as $ev): ?>
    <li><?= e($ev['created_at']) ?> — <?= e($ev['to_status']) ?><?= $ev['note'] ? ' (' . e($ev['note']) . ')' : '' ?></li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>

  <div style="display:flex;flex-wrap:wrap;gap:.75rem;margin-top:1.5rem">
    <?php if ($order['status'] === 'pending'): ?>
    <a class="xd-btn" href="<?= e(url('/paiement/' . $order['id'])) ?>">Payer</a>
    <?php endif; ?>
    <?php if (in_array($order['status'], ['pending', 'awaiting_wire', 'awaiting_paypal', 'cod_confirmed'], true)): ?>
    <form method="post" action="<?= e(url('/commande/' . $order['id'] . '/annuler')) ?>" onsubmit="return confirm('Annuler cette commande ?');">
      <?= csrf_field() ?>
      <button type="submit" class="xd-btn xd-btn--ghost">Annuler</button>
    </form>
    <?php endif; ?>
    <form method="post" action="<?= e(url('/commande/' . $order['id'] . '/recommander')) ?>">
      <?= csrf_field() ?>
      <button type="submit" class="xd-btn xd-btn--ghost">Recommander</button>
    </form>
  </div>
</section>
