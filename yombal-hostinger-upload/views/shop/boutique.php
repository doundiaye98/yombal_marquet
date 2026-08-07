<?php $boutique_photo_slides = ['img/yombal-catalogue-hero.jpg','img/gallery-catalogue-riz-farines.jpg','img/gallery-catalogue-huiles-condiments.jpg','img/gallery-catalogue-snacks-boissons.jpg','img/gallery-catalogue-produits-mer.jpg','img/gallery-catalogue-cosmetique-beaute.jpg','img/gallery-catalogue-chaussures-sacs.jpg']; ?>
<div class="page-wrapper boutique-page boutique-page--home">
  <header class="boutique-hero boutique-hero--catalog">
    <div class="boutique-hero__inner"><p class="boutique-hero__eyebrow">Yombal Market · Catalogue</p><h1 class="boutique-hero__title">Le goût <em>du vrai</em></h1><p class="boutique-hero__lead">Riz, farines, huiles, snacks, boissons, produits de la mer, cosmétique, électronique, électroménager, mode, chaussures et sacs — une sélection diaspora et marketplace, livrée chez vous.</p><div class="boutique-hero__stats"><span><strong><?= (int) $total_products ?></strong> références</span><span class="boutique-hero__dot" aria-hidden="true"></span><span>Livraison suivie</span><span class="boutique-hero__dot" aria-hidden="true"></span><span>Prix TTC catalogue</span></div></div>
  </header>

  <section class="boutique-catalog" aria-label="Catalogue">
    <div class="boutique-catalog__bg boutique-catalog__bg--slideshow" aria-hidden="true" data-boutique-slideshow data-interval="5000"><div class="boutique-catalog__track" data-boutique-track><?php foreach ($boutique_photo_slides as $slide): ?><div class="boutique-catalog__slide" style="background-image: url('<?= e(asset($slide)) ?>')"></div><?php endforeach; ?><div class="boutique-catalog__slide" style="background-image: url('<?= e(asset($boutique_photo_slides[0])) ?>')"></div></div></div>
    <div class="boutique-shell">
      <aside class="boutique-sidebar" aria-label="Filtrer le catalogue">
        <div class="boutique-sidebar__panel">
          <p class="boutique-sidebar__label">Univers boutique</p>
          <nav class="boutique-universe-nav" aria-label="Alimentaire ou non alimentaire">
            <a href="<?= e(url('/boutique')) ?>" class="boutique-universe-link <?= !$filter_type && !$filter_cat ? 'is-active' : '' ?>"><span>✦ Tout le catalogue</span><span class="boutique-universe-link__count"><?= (int) $total_products ?></span></a>
            <a href="<?= e(url('/boutique?type=alimentaire')) ?>" class="boutique-universe-link <?= $filter_type === 'alimentaire' && !$filter_cat ? 'is-active' : '' ?>"><span><?= e($shop_universe_labels['alimentaire']['emoji']) ?> <?= e($shop_universe_labels['alimentaire']['label']) ?></span><span class="boutique-universe-link__count"><?= (int) ($universe_counts['alimentaire'] ?? 0) ?></span></a>
            <a href="<?= e(url('/boutique?type=non-alimentaire')) ?>" class="boutique-universe-link <?= $filter_type === 'non-alimentaire' && !$filter_cat ? 'is-active' : '' ?>"><span><?= e($shop_universe_labels['non-alimentaire']['emoji']) ?> <?= e($shop_universe_labels['non-alimentaire']['label']) ?></span><span class="boutique-universe-link__count"><?= (int) ($universe_counts['non-alimentaire'] ?? 0) ?></span></a>
          </nav>
          <p class="boutique-sidebar__label boutique-sidebar__label--spaced">Rayons</p>
          <nav class="boutique-cat-nav">
            <?php foreach ($shop_rayons as $cat_key): if (($shop_counts[$cat_key] ?? 0) > 0): $meta = $product_categories[$cat_key] ?? ['label' => $cat_key, 'emoji' => '🛒']; ?>
            <a href="<?= e($filter_type ? url('/boutique?categorie=' . urlencode($cat_key) . '&type=' . urlencode($filter_type)) : url('/boutique?categorie=' . urlencode($cat_key))) ?>" class="boutique-cat-link <?= $filter_cat === $cat_key ? 'is-active' : '' ?>"><span class="boutique-cat-link__emoji" aria-hidden="true"><?= e($meta['emoji']) ?></span><span class="boutique-cat-link__text"><?= e($meta['label']) ?></span><span class="boutique-cat-link__count"><?= (int) $shop_counts[$cat_key] ?></span></a>
            <?php endif; endforeach; ?>
          </nav>
        </div>
      </aside>

      <main class="boutique-main">
        <?php if ($catalog_sections): ?>
          <?php foreach ($catalog_sections as $section): $meta = $product_categories[$section['key']] ?? ['label' => 'Autres', 'emoji' => '🛒']; ?>
          <section class="catalog-rayon" id="rayon-<?= e($section['key']) ?>">
            <header class="catalog-rayon__head"><h2 class="catalog-rayon__title"><span aria-hidden="true"><?= e($meta['emoji']) ?></span><?= e($meta['label']) ?></h2><span class="catalog-rayon__count"><?= count($section['entries']) ?> réf.</span></header>
            <div class="boutique-grid">
              <?php foreach ($section['entries'] as $entry): $p = $entry['product']; $meta2 = $product_categories[$p['category']] ?? ['label' => $p['category'], 'emoji' => '🛒']; ?>
              <article class="boutique-card"><a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="boutique-card__media<?= !empty($p['image']) ? ' boutique-card__media--photo' : '' ?>"><?= render_product_image($p, 'card') ?><span class="boutique-card__cat"><?= e($meta2['emoji']) ?> <?= e($meta2['label']) ?></span></a><div class="boutique-card__body"><h3 class="boutique-card__title"><a href="<?= e(url('/produit/' . $p['slug'])) ?>"><?= e($p['name']) ?></a></h3><?php if (!empty($p['weight_info'])): ?><p class="boutique-card__meta"><?= e($p['weight_info']) ?></p><?php endif; ?><div class="boutique-card__footer"><?= catalog_price_badge(price_euros($p)) ?><div class="boutique-card__actions"><a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="boutique-card__link">Fiche</a><form method="post" action="<?= e(url('/panier/ajouter')) ?>" class="boutique-card__form"><?= csrf_field() ?><input type="hidden" name="product_id" value="<?= (int) $p['id'] ?>"><input type="hidden" name="quantity" value="1"><button type="submit" class="boutique-card__cart" title="Ajouter au panier" aria-label="Ajouter <?= e($p['name']) ?> au panier">+</button></form></div></div></div></article>
              <?php endforeach; ?>
            </div>
          </section>
          <?php endforeach; ?>
        <?php elseif ($catalog): ?>
        <div class="boutique-toolbar"><div><h2 class="boutique-toolbar__title"><?php if ($filter_cat && isset($product_categories[$filter_cat])): ?><?= e($product_categories[$filter_cat]['emoji']) ?> <?= e($product_categories[$filter_cat]['label']) ?><?php elseif ($filter_type === 'alimentaire'): ?><?= e($shop_universe_labels['alimentaire']['emoji']) ?> <?= e($shop_universe_labels['alimentaire']['label']) ?><?php elseif ($filter_type === 'non-alimentaire'): ?><?= e($shop_universe_labels['non-alimentaire']['emoji']) ?> <?= e($shop_universe_labels['non-alimentaire']['label']) ?><?php else: ?>Tout le catalogue<?php endif; ?></h2><p class="boutique-toolbar__meta"><strong><?= count($catalog) ?></strong> référence<?= count($catalog) > 1 ? 's' : '' ?></p></div></div>
        <div class="boutique-grid">
          <?php foreach ($catalog as $entry): $p = $entry['product']; $meta = $product_categories[$p['category']] ?? ['label' => $p['category'], 'emoji' => '🛒']; ?>
          <article class="boutique-card"><a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="boutique-card__media<?= !empty($p['image']) ? ' boutique-card__media--photo' : '' ?>"><?= render_product_image($p, 'card') ?><span class="boutique-card__cat"><?= e($meta['emoji']) ?> <?= e($meta['label']) ?></span></a><div class="boutique-card__body"><h3 class="boutique-card__title"><a href="<?= e(url('/produit/' . $p['slug'])) ?>"><?= e($p['name']) ?></a></h3><?php if (!empty($p['weight_info'])): ?><p class="boutique-card__meta"><?= e($p['weight_info']) ?></p><?php endif; ?><div class="boutique-card__footer"><?= catalog_price_badge(price_euros($p)) ?><div class="boutique-card__actions"><a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="boutique-card__link">Fiche</a><form method="post" action="<?= e(url('/panier/ajouter')) ?>" class="boutique-card__form"><?= csrf_field() ?><input type="hidden" name="product_id" value="<?= (int) $p['id'] ?>"><input type="hidden" name="quantity" value="1"><button type="submit" class="boutique-card__cart" title="Ajouter au panier" aria-label="Ajouter <?= e($p['name']) ?> au panier">+</button></form></div></div></div></article>
          <?php endforeach; ?>
        </div>
        <?php else: ?>
        <div class="boutique-empty"><p class="boutique-empty__title">Aucun produit dans ce rayon</p><p class="boutique-empty__hint">Essayez une autre catégorie ou parcourez tout le catalogue.</p><a href="<?= e(url('/boutique')) ?>" class="btn-primary">Voir tout le catalogue</a></div>
        <?php endif; ?>
      </main>
    </div>
  </section>
</div>
<script>
(function () {
  var root = document.querySelector("[data-boutique-slideshow]");
  if (!root) return;
  var track = root.querySelector("[data-boutique-track]");
  var slides = root.querySelectorAll(".boutique-catalog__slide");
  if (!track || slides.length < 2) return;
  var realCount = slides.length - 1, interval = parseInt(root.getAttribute("data-interval") || "5000", 10), index = 0, moving = false, reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function setX(i, animate) { track.style.transition = (!animate || reduced) ? "none" : ""; track.style.transform = "translate3d(-" + i * 100 + "%, 0, 0)"; }
  track.addEventListener("transitionend", function (e) { if (e.target !== track || e.propertyName !== "transform") return; if (index < realCount) { moving = false; return; } setX(0, false); void track.offsetWidth; track.style.transition = ""; index = 0; moving = false; });
  setInterval(function () { if (moving && !reduced) return; moving = true; index += 1; setX(index, true); if (reduced && index >= realCount) { index = 0; setX(0, false); moving = false; } }, interval);
})();
</script>
