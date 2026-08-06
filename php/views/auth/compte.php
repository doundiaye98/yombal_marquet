<section class="section-block">
  <div class="section-head">
    <h1>Mon compte</h1>
    <p><?= e($user['name'] ?: $user['email']) ?></p>
  </div>
  <h2>Mes commandes</h2>
  <?php if (!$orders): ?>
  <p>Aucune commande pour le moment. <a href="<?= e(url('/boutique')) ?>">Boutique</a></p>
  <?php else: ?>
  <ul>
    <?php foreach ($orders as $o): ?>
    <li>
      <a href="<?= e(url('/suivi-commande/' . $o['id'])) ?>"><strong><?= e($o['public_ref']) ?></strong></a>
      — <?= e(money_eur((int) $o['total_cents'])) ?>
      — <?= e(order_status_label($o['status'])) ?>
      — <?= e($o['created_at']) ?>
    </li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>
</section>
