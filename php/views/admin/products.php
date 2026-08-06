<?php require __DIR__ . '/_nav.php'; ?>
<section class="section-block">
  <div class="section-head">
    <h1>Produits</h1>
    <a class="xd-btn" href="<?= e(url('/admin/produit/nouveau')) ?>">Nouveau</a>
  </div>
  <table style="width:100%;border-collapse:collapse">
    <thead><tr><th align="left">Nom</th><th>Catégorie</th><th>Prix</th><th>Actif</th><th></th></tr></thead>
    <tbody>
      <?php foreach ($products as $p): ?>
      <tr>
        <td><?= e($p['name']) ?></td>
        <td><?= e($p['category']) ?></td>
        <td><?= e(money_eur((int) $p['price_cents'])) ?></td>
        <td><?= $p['is_active'] ? 'oui' : 'non' ?></td>
        <td><a href="<?= e(url('/admin/produit/' . $p['id'])) ?>">Éditer</a></td>
      </tr>
      <?php endforeach; ?>
    </tbody>
  </table>
</section>
