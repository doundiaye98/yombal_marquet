<?php require __DIR__ . '/_nav.php'; ?>
<section class="section-block">
  <h1>Administration</h1>
  <ul>
    <li>Commandes : <?= (int) $stats['orders'] ?></li>
    <li>Produits actifs : <?= (int) $stats['products'] ?></li>
    <li>Messages non lus : <?= (int) $stats['unread'] ?></li>
  </ul>
  <h2>Dernières commandes</h2>
  <ul>
    <?php foreach ($recent as $o): ?>
    <li><a href="<?= e(url('/admin/commande/' . $o['id'])) ?>"><?= e($o['public_ref']) ?></a> — <?= e(order_status_label($o['status'])) ?> — <?= e(money_eur((int) $o['total_cents'])) ?></li>
    <?php endforeach; ?>
  </ul>
</section>
