<div class="page-wrapper order-flow-page<?= $items ? ' has-cart-sticky' : '' ?>">
  <?= checkout_steps('cart') ?>
  <header class="page-hero page-hero--compact">
    <p class="section-eyebrow reveal">Panier</p>
    <h1 class="section-title reveal">Vos <em>articles</em><?php if ($cart_item_count): ?> <span class="cart-count-badge"><?= (int) $cart_item_count ?></span><?php endif; ?></h1>
    <p class="section-sub reveal">Modifiez les quantités puis validez — <strong>commande possible sans créer de compte</strong>.</p>
  </header>
  <section class="section section--cart section--flush-top">
    <?php if ($items): ?>
    <?= order_trust_panel('cart') ?>
    <ul class="cart-list reveal">
      <?php foreach ($items as $row): $p = $row['product']; ?>
      <li class="cart-item">
        <div class="cart-item-media<?= !empty($p['image']) ? ' cart-item-media--photo' : '' ?>"><?= render_product_image($p, 'thumb') ?></div>
        <div class="cart-item-info"><a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="cart-item-title"><?= e($p['name']) ?></a><p class="cart-item-unit-line"><span class="cart-item-price-unit"><?= e(number_format(price_euros($p), 2, '.', '')) ?> €</span><span class="cart-item-unit-suffix">/ unité</span></p></div>
        <div class="cart-item-qty-wrap"><label class="cart-item-qty-label" for="qty-<?= (int) $p['id'] ?>">Qté</label><form class="cart-item-qty-form" method="post" action="<?= e(url('/panier/modifier')) ?>"><?= csrf_field() ?><input type="hidden" name="product_id" value="<?= (int) $p['id'] ?>"><input id="qty-<?= (int) $p['id'] ?>" class="cart-item-qty-input" type="number" name="quantity" value="<?= (int) $row['quantity'] ?>" min="1" max="99" inputmode="numeric" autocomplete="off"><button type="submit" class="cart-item-update">OK</button></form></div>
        <div class="cart-item-subtotal-wrap"><span class="cart-item-sub-label">Sous-total</span><strong class="cart-item-sub-amount"><?= e(number_format($row['line_total_cents'] / 100, 2, '.', '')) ?> €</strong></div>
        <form class="cart-item-remove-form" method="post" action="<?= e(url('/panier/modifier')) ?>"><?= csrf_field() ?><input type="hidden" name="product_id" value="<?= (int) $p['id'] ?>"><input type="hidden" name="quantity" value="0"><button type="submit" class="cart-item-remove"><span class="cart-item-remove-icon" aria-hidden="true">×</span>Retirer</button></form>
      </li>
      <?php endforeach; ?>
    </ul>
    <div class="cart-summary reveal"><div class="cart-summary-row"><span class="cart-summary-label">Total TTC <span class="cart-summary-hint">(<?= (int) $cart_item_count ?> article<?= $cart_item_count > 1 ? 's' : '' ?>)</span></span><span class="cart-summary-total"><?= e(number_format($total_cents / 100, 2, '.', '')) ?> €</span></div><p class="cart-summary-trust-note">Sans compte · Livraison <?= e($shop_settings['shop_delivery_days_min']) ?>–<?= e($shop_settings['shop_delivery_days_max']) ?> j. · Carte, PayPal, virement ou espèces</p><div class="cart-summary-actions cart-summary-actions--desktop"><a href="<?= e(url('/checkout')) ?>" class="btn-primary">Passer commande</a><a href="<?= e(url('/boutique')) ?>" class="btn-outline">Continuer les achats</a></div></div>
    <div class="cart-sticky-bar" role="region" aria-label="Récapitulatif panier"><div class="cart-sticky-bar-inner"><div class="cart-sticky-bar-meta"><span class="cart-sticky-bar-label"><?= (int) $cart_item_count ?> article<?= $cart_item_count > 1 ? 's' : '' ?></span><strong class="cart-sticky-bar-total"><?= e(number_format($total_cents / 100, 2, '.', '')) ?> €</strong></div><a href="<?= e(url('/checkout')) ?>" class="btn-primary">Commander</a></div></div>
    <?php else: ?>
    <p class="section-sub reveal">Votre panier est vide.</p>
    <a href="<?= e(url('/boutique')) ?>" class="btn-primary reveal">Découvrir la boutique</a>
    <?php endif; ?>
  </section>
</div>
