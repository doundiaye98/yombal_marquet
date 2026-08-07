<?php require __DIR__ . '/_nav.php'; ?>
<section class="section-block" style="max-width:640px">
  <h1><?= $product ? 'Modifier' : 'Nouveau' ?> produit</h1>
  <form method="post">
    <?= csrf_field() ?>
    <label>Nom *<input name="name" required value="<?= e($product['name'] ?? '') ?>"></label>
    <label>Slug *<input name="slug" required value="<?= e($product['slug'] ?? '') ?>"></label>
    <label>SKU<input name="sku" value="<?= e($product['sku'] ?? '') ?>"></label>
    <label>Prix (€) *<input name="price_euros" required value="<?= e(isset($product) ? number_format(((int)$product['price_cents'])/100, 2, '.', '') : '0.00') ?>"></label>
    <label>Catégorie
      <select name="category">
        <?php foreach ($categories as $slug => $label): ?>
        <option value="<?= e($slug) ?>" <?= (($product['category'] ?? '') === $slug) ? 'selected' : '' ?>><?= e($label) ?></option>
        <?php endforeach; ?>
      </select>
    </label>
    <label>Résumé<input name="summary" value="<?= e($product['summary'] ?? '') ?>"></label>
    <label>Description *<textarea name="description" rows="6" required><?= e($product['description'] ?? '') ?></textarea></label>
    <label>Image (chemin sous static/, ex. img/products/xxx.jpg)<input name="image" value="<?= e($product['image'] ?? '') ?>"></label>
    <label>Origine<input name="origin" value="<?= e($product['origin'] ?? '') ?>"></label>
    <label>Poids / format<input name="weight_info" value="<?= e($product['weight_info'] ?? '') ?>"></label>
    <label>Stock (vide = illimité)<input name="stock_qty" value="<?= e(isset($product['stock_qty']) && $product['stock_qty'] !== null ? (string)$product['stock_qty'] : '') ?>"></label>
    <label>Icône emoji<input name="icon" value="<?= e($product['icon'] ?? '') ?>"></label>
    <label><input type="checkbox" name="is_active" <?= !isset($product) || !empty($product['is_active']) ? 'checked' : '' ?>> Actif</label>
    <button type="submit" class="xd-btn">Enregistrer</button>
  </form>
  <?php if ($product): ?>
  <form method="post" action="<?= e(url('/admin/produit/' . $product['id'] . '/supprimer')) ?>" style="margin-top:1rem" onsubmit="return confirm('Désactiver ce produit ?');">
    <?= csrf_field() ?>
    <button type="submit" class="xd-btn xd-btn--ghost">Désactiver</button>
  </form>
  <?php endif; ?>
</section>
<style>label{display:block;margin:1rem 0}input,textarea,select{width:100%;padding:.5rem;margin-top:.25rem}</style>
