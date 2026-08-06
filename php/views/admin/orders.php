<?php require __DIR__ . '/_nav.php'; ?>
<section class="section-block">
  <h1>Commandes</h1>
  <table style="width:100%;border-collapse:collapse">
    <thead><tr><th align="left">Réf</th><th>Statut</th><th>Total</th><th>Date</th></tr></thead>
    <tbody>
      <?php foreach ($orders as $o): ?>
      <tr>
        <td><a href="<?= e(url('/admin/commande/' . $o['id'])) ?>"><?= e($o['public_ref']) ?></a></td>
        <td><?= e(order_status_label($o['status'])) ?></td>
        <td><?= e(money_eur((int) $o['total_cents'])) ?></td>
        <td><?= e($o['created_at']) ?></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</section>
