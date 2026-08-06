<section class="section-block product-detail">
  <div class="product-detail__grid" style="display:grid;gap:2rem;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr)">
    <div>
      <img src="<?= e(product_image_url($product['image'] ?? null)) ?>" alt="<?= e($product['name']) ?>" style="width:100%;max-width:520px;border-radius:8px;object-fit:cover" width="520" height="520">
    </div>
    <div>
      <p class="eyebrow"><?= e(category_labels()[$product['category']] ?? $product['category']) ?></p>
      <h1><?= e($product['name']) ?></h1>
      <p class="product-card__price" style="font-size:1.4rem"><?= e(money_eur((int) $product['price_cents'])) ?></p>
      <?php if (!empty($product['summary'])): ?><p><?= e($product['summary']) ?></p><?php endif; ?>
      <div class="prose"><?= nl2br(e($product['description'])) ?></div>
      <?php if (!empty($product['weight_info'])): ?><p><strong>Conditionnement :</strong> <?= e($product['weight_info']) ?></p><?php endif; ?>
      <?php if (!empty($product['origin'])): ?><p><strong>Origine :</strong> <?= e($product['origin']) ?></p><?php endif; ?>
      <form method="post" action="<?= e(url('/panier/ajouter')) ?>" style="margin-top:1.5rem;display:flex;gap:.75rem;align-items:center">
        <?= csrf_field() ?>
        <input type="hidden" name="product_id" value="<?= (int) $product['id'] ?>">
        <label>Qté <input type="number" name="quantity" value="1" min="1" max="99" style="width:4rem"></label>
        <button type="submit" class="xd-btn">Ajouter au panier</button>
      </form>
    </div>
  </div>

  <?php if ($related): ?>
  <div class="section-head" style="margin-top:3rem">
    <h2>Vous aimerez aussi</h2>
  </div>
  <div class="product-grid">
    <?php foreach ($related as $p): ?>
    <article class="product-card">
      <a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="product-card__media">
        <img src="<?= e(product_image_url($p['image'] ?? null)) ?>" alt="<?= e($p['name']) ?>" loading="lazy">
      </a>
      <div class="product-card__body">
        <h3><a href="<?= e(url('/produit/' . $p['slug'])) ?>"><?= e($p['name']) ?></a></h3>
        <p class="product-card__price"><?= e(money_eur((int) $p['price_cents'])) ?></p>
      </div>
    </article>
    <?php endforeach; ?>
  </div>
  <?php endif; ?>
</section>
