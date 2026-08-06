<?php $home_photo_slides = ['img/yombal-mobile-livraison.jpg','img/yombal-mobile-commande.jpg','img/yombal-mobile-univers.jpg','img/yombal-mobile-hero-2.jpg','img/yombal-mobile-hero.jpg']; $rays = [['cereales','Céréales','🌾'],['legumineuses','Légumineuses','🫘'],['huiles','Huiles & graisses','🫒'],['snacks','Snacks','🥨'],['desserts','Desserts','🍮'],['boissons','Boissons & sirops','🥤'],['condiments','Condiments','🧂'],['fruits','Fruits','🍊'],['legumes','Légumes','🥬'],['conserves','Conserves','🫙'],['poisson','Produits de la mer','🐟'],['viandes','Viandes & volailles','🍗'],['cosmetique','Cosmétique','✨'],['electronique','Électronique','📱'],['electromenager','Électroménager','🏠'],['mode','Habillement','👕'],['chaussures','Chaussures','👟'],['bagagerie','Sacs & bagagerie','🎒']]; ?>
<div class="home-page">
  <div class="home-page__bg home-page__bg--slideshow" aria-hidden="true" data-home-slideshow data-interval="5000">
    <div class="home-page__track" data-home-track>
      <?php foreach ($home_photo_slides as $slide): ?><div class="home-page__slide" style="background-image: url('<?= e(asset($slide)) ?>')"></div><?php endforeach; ?>
      <div class="home-page__slide" style="background-image: url('<?= e(asset($home_photo_slides[0])) ?>')"></div>
    </div>
  </div>

  <div class="home-page__content">
    <section class="xd-hero xd-hero--home" aria-label="Accueil Yombal Market">
      <div class="xd-hero__scrim" aria-hidden="true"></div>
      <div class="xd-hero__body"><div class="xd-hero__copy"><p class="xd-hero__brand">Yombal Market</p><h1 class="xd-hero__title">Votre marché<br><em>en poche.</em></h1><p class="xd-hero__lead">Le vrai local, là où vous êtes.<br>Commandez. Recevez.</p><div class="xd-hero__cta"><a href="<?= e(url('/boutique')) ?>" class="xd-btn xd-btn--light">Ouvrir la boutique</a><a href="<?= e(url('/recettes')) ?>" class="xd-btn xd-btn--ghost">Découvrir les saveurs</a></div></div></div>
    </section>

    <section class="home-rayons" id="rayons" aria-label="Rayons boutique">
      <div class="home-rayons__inner">
        <header class="home-rayons__head"><p class="home-rayons__kicker">01 — Boutique</p><h2 class="home-rayons__title">Nos <em>rayons</em></h2><p class="home-rayons__lead">Riz, huiles, épices, électronique, mode, électroménager… choisissez votre univers en un clic.</p></header>
        <a href="<?= e(url('/boutique')) ?>" class="home-rayons__featured"><span class="home-rayons__featured-label">Tout le catalogue</span><span class="home-rayons__featured-meta"><?= (int) $product_count ?> références</span><span class="home-rayons__featured-go" aria-hidden="true">→</span></a>
        <ul class="home-rayons__list">
          <?php foreach ($rays as [$key, $label, $emoji]): ?><li><a href="<?= e(url('/boutique?categorie=' . urlencode($key))) ?>" class="home-rayons__link"><span class="home-rayons__emoji" aria-hidden="true"><?= e($emoji) ?></span><span class="home-rayons__name"><?= e($label) ?></span><span class="home-rayons__arrow" aria-hidden="true">→</span></a></li><?php endforeach; ?>
        </ul>
      </div>
    </section>

    <?php if ($catalogue_phares): ?>
    <section class="xd-highlights xd-highlights--home" aria-label="Produits incontournables">
      <div class="xd-highlights__inner">
        <header class="xd-section-head xd-reveal"><span class="xd-section-num">02</span><div><p class="xd-eyebrow">Sélection</p><h2 class="xd-section-title">Les <em>incontournables</em></h2><p class="xd-section-sub">Thiakry, Fonio, Arraw, Baobab… le meilleur du terroir, sélectionné pour vous.</p></div><a href="<?= e(url('/boutique')) ?>" class="xd-btn xd-btn--outline">Toute la boutique</a></header>
        <div class="xd-highlights__grid">
          <?php foreach ($catalogue_phares as $idx => $p): $meta = $product_categories[$p['category']] ?? ['label' => $p['category'], 'emoji' => '🛒']; ?>
          <article class="xd-product xd-product--premium xd-highlights__card xd-reveal" style="--stagger: <?= e(number_format($idx * 0.07, 2, '.', '')) ?>s"><div class="xd-product__shine" aria-hidden="true"></div><span class="xd-product__index"><?= e(sprintf('%02d', $idx + 1)) ?></span><a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="xd-product__media<?= !empty($p['image']) ? ' xd-product__media--photo' : '' ?>"><?= render_product_image($p, 'card') ?><span class="xd-product__cat"><?= e($meta['emoji']) ?> <?= e($meta['label']) ?></span></a><div class="xd-product__body"><h3><a href="<?= e(url('/produit/' . $p['slug'])) ?>"><?= e($p['name']) ?></a></h3><?php if (!empty($p['weight_info'])): ?><p class="xd-highlights__weight"><?= e($p['weight_info']) ?></p><?php endif; ?><div class="xd-product__foot"><span class="xd-product__price"><?= e(number_format(price_euros($p), 2, '.', '')) ?> €</span><form method="post" action="<?= e(url('/panier/ajouter')) ?>"><?= csrf_field() ?><input type="hidden" name="product_id" value="<?= (int) $p['id'] ?>"><input type="hidden" name="quantity" value="1"><button type="submit" class="xd-product__add" aria-label="Ajouter <?= e($p['name']) ?> au panier"><span aria-hidden="true">+</span></button></form></div></div></article>
          <?php endforeach; ?>
        </div>
      </div>
    </section>
    <?php endif; ?>

    <div class="xd-marquee" aria-hidden="true"><div class="xd-marquee__track"><span>Épicerie fine</span><span class="xd-marquee__sep">✦</span><span>Produits locaux</span><span class="xd-marquee__sep">✦</span><span>Livraison suivie</span><span class="xd-marquee__sep">✦</span><span>Sans compte</span><span class="xd-marquee__sep">✦</span><span>Diaspora</span><span class="xd-marquee__sep">✦</span><span>Épicerie fine</span><span class="xd-marquee__sep">✦</span><span>Produits locaux</span><span class="xd-marquee__sep">✦</span><span>Livraison suivie</span><span class="xd-marquee__sep">✦</span><span>Sans compte</span><span class="xd-marquee__sep">✦</span><span>Diaspora</span><span class="xd-marquee__sep">✦</span></div></div>

    <?php if (!empty($featured_recipes)): ?>
    <section class="ud-panel ud-panel--green" aria-label="Recettes"><header class="ud-panel__head"><p class="section-eyebrow">Cuisine</p><h2 class="section-title">Paniers <em>intelligents</em></h2><a href="<?= e(url('/recettes')) ?>" class="ud-btn ud-btn--outline ud-btn--sm">Toutes les recettes</a></header><div class="ud-cards"><?php foreach ($featured_recipes as $recipe): ?><article class="ud-card"><span class="ud-card__emoji" aria-hidden="true"><?= e($recipe['emoji']) ?></span><p class="ud-card__kind"><?= e($recipe['kind_label']) ?></p><h3><a href="<?= e(url('/recette/' . $recipe['slug'])) ?>"><?= e($recipe['title']) ?></a></h3><p><?= e($recipe['summary'] ?? '') ?></p><div class="ud-card__foot"><span>dès <?= e(number_format(((int) ($recipe['total_cents'] ?? 0)) / 100, 2, '.', '')) ?> €</span><a href="<?= e(url('/recette/' . $recipe['slug'])) ?>">Voir →</a></div></article><?php endforeach; ?></div></section>
    <?php endif; ?>

    <section class="ud-cta" aria-label="Commander"><div class="ud-cta__inner"><h2>Prêt à commander<br><em>le vrai marché ?</em></h2><p>Livraison suivie · Paiement sécurisé · Prix catalogue officiel</p><div class="ud-cta__actions"><a href="<?= e(url('/boutique')) ?>" class="ud-btn ud-btn--gold">Ouvrir la boutique</a><a href="<?= e(url('/contact')) ?>" class="ud-btn ud-btn--outline">Nous contacter</a></div></div></section>
  </div>
</div>
<script>
(function () {
  var root = document.querySelector("[data-home-slideshow]");
  if (!root) return;
  var track = root.querySelector("[data-home-track]");
  var slides = root.querySelectorAll(".home-page__slide");
  if (!track || slides.length < 2) return;
  var realCount = slides.length - 1;
  var interval = parseInt(root.getAttribute("data-interval") || "5000", 10);
  var index = 0;
  var moving = false;
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function setX(i, animate) { track.style.transition = (!animate || reduced) ? "none" : ""; track.style.transform = "translate3d(-" + i * 100 + "%, 0, 0)"; }
  track.addEventListener("transitionend", function (e) { if (e.target !== track || e.propertyName !== "transform") return; if (index < realCount) { moving = false; return; } setX(0, false); void track.offsetWidth; track.style.transition = ""; index = 0; moving = false; });
  setInterval(function () { if (moving && !reduced) return; moving = true; index += 1; setX(index, true); if (reduced && index >= realCount) { index = 0; setX(0, false); moving = false; } }, interval);
})();
</script>
