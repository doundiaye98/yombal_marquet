<?php
$slug = $service['slug'];
$has_form = in_array($slug, EcosystemData::FORM_SLUGS, true);
$slides = EcosystemData::slideshows()[$slug] ?? null;
$photo_bg = EcosystemData::photoBg($slug);
$has_photo = $slides || $photo_bg;
$hub_services = ($slug === 'autres-services') ? ecosystem_hub_services() : null;
$extra_css = $extra_css ?? '';
?>
<div class="page-wrapper ecosystem-page<?= $has_form ? ' ecosystem-page--with-form' : '' ?><?= $has_photo ? ' ecosystem-page--photo ecosystem-page--' . e($slug) : '' ?>">
  <header class="ecosystem-hero ecosystem-hero--<?= e($slug) ?>">
    <div class="ecosystem-hero__inner">
      <span class="ecosystem-hero__icon" aria-hidden="true"><?= e($service['icon']) ?></span>
      <p class="ecosystem-hero__eyebrow">Groupe YOMBAL</p>
      <h1 class="ecosystem-hero__title"><?= e($service['title']) ?></h1>
      <p class="ecosystem-hero__tagline"><?= e($service['tagline']) ?></p>
      <p class="ecosystem-hero__lead"><?= e($service['lead']) ?></p>
      <?php if (!empty($service['boutique_category'])): ?>
      <div class="ecosystem-hero__cta-row">
        <a href="<?= !empty($boutique_products) ? '#catalogue-boutique' : e(url('/boutique?type=non-alimentaire&categorie=' . urlencode($service['boutique_category']))) ?>" class="btn-primary ecosystem-hero__cta"><?= e($service['cta_label']) ?></a>
        <?php if ($has_form): ?><a href="#demande-form" class="btn-outline ecosystem-hero__cta ecosystem-hero__cta--secondary">Nous contacter</a><?php endif; ?>
      </div>
      <?php elseif ($has_form): ?>
      <a href="#demande-form" class="btn-primary ecosystem-hero__cta"><?= e($service['cta_label']) ?></a>
      <?php elseif (!empty($service['external_url'])): ?>
      <a href="<?= e($service['external_url']) ?>" class="btn-primary ecosystem-hero__cta" target="_blank" rel="noopener noreferrer"><?= e($service['cta_label']) ?> ↗</a>
      <?php else: ?>
      <a href="<?= e(url('/contact')) ?>" class="btn-primary ecosystem-hero__cta"><?= e($service['cta_label']) ?></a>
      <?php endif; ?>
    </div>
  </header>

  <div class="ecosystem-body<?= $has_photo ? ' ecosystem-body--photo' : '' ?>">
    <?php if ($slides): ?>
    <div class="ecosystem-body__bg ecosystem-body__bg--slideshow" aria-hidden="true" data-ecosystem-slideshow data-interval="5000">
      <div class="ecosystem-body__track" data-ecosystem-track>
        <?php foreach ($slides as $slide): ?><div class="ecosystem-body__slide" style="background-image: url('<?= e(asset($slide)) ?>')"></div><?php endforeach; ?>
        <div class="ecosystem-body__slide" style="background-image: url('<?= e(asset($slides[0])) ?>')"></div>
      </div>
    </div>
    <?php elseif ($photo_bg): ?>
    <div class="ecosystem-body__bg" aria-hidden="true" style="background-image: url('<?= e(asset($photo_bg)) ?>')"></div>
    <?php endif; ?>

    <div class="ecosystem-body__content">
      <?php if ($hub_services): ?>
      <section class="section ecosystem-hub">
        <div class="ecosystem-hub__inner">
          <p class="section-eyebrow">Groupe YOMBAL</p>
          <h2 class="ecosystem-hub__title">Tous nos services</h2>
          <p class="ecosystem-hub__lead">Une demande, une équipe — choisissez le service qui vous concerne ou utilisez le formulaire ci-dessous.</p>
          <div class="ecosystem-hub__grid">
            <?php foreach ($hub_services as $item): ?>
            <article class="ecosystem-hub__card">
              <span class="ecosystem-hub__icon" aria-hidden="true"><?= e($item['icon']) ?></span>
              <h3><?= e($item['short_label']) ?></h3>
              <p><?= e($item['tagline'] ?? '') ?></p>
              <?php if (!empty($item['external_url'])): ?>
              <a href="<?= e($item['external_url']) ?>" class="ecosystem-hub__link" target="_blank" rel="noopener noreferrer">Découvrir ↗</a>
              <?php elseif ($item['slug'] === 'immobilier-btp'): ?>
              <a href="<?= e(url('/ecosysteme/immobilier-btp')) ?>" class="ecosystem-hub__link">Voir le programme</a>
              <?php elseif (in_array($item['slug'], EcosystemData::FORM_SLUGS, true)): ?>
              <a href="<?= e(url('/ecosysteme/' . $item['slug'])) ?>#demande-form" class="ecosystem-hub__link">Faire une demande</a>
              <?php else: ?>
              <a href="<?= e(url('/ecosysteme/' . $item['slug'])) ?>" class="ecosystem-hub__link">En savoir plus</a>
              <?php endif; ?>
            </article>
            <?php endforeach; ?>
          </div>
        </div>
      </section>
      <?php endif; ?>

      <section class="section ecosystem-detail">
        <div class="ecosystem-detail__grid">
          <div class="ecosystem-detail__card">
            <h2>Ce que nous proposons</h2>
            <ul class="ecosystem-detail__list"><?php foreach ($service['bullets'] as $item): ?><li><?= e($item) ?></li><?php endforeach; ?></ul>
          </div>
          <aside class="ecosystem-detail__aside">
            <h3>Besoin d'aide ?</h3>
            <p>Notre équipe vous répond pour un devis, une réservation ou une question.</p>
            <a href="mailto:<?= e($shop_contact_email) ?>" class="email-chip"><?= e($shop_contact_email) ?></a>
            <?php if ($has_form): ?><a href="#demande-form" class="btn-primary ecosystem-detail__form">Envoyer une demande</a><?php endif; ?>
            <?php if (!empty($service['boutique_category'])): ?>
            <a href="<?= e(url('/boutique?type=non-alimentaire&categorie=' . urlencode($service['boutique_category']))) ?>" class="btn-outline ecosystem-detail__shop">Voir toute la boutique</a>
            <?php else: ?>
            <a href="<?= e(url('/boutique')) ?>" class="btn-outline ecosystem-detail__shop">Voir la boutique</a>
            <?php endif; ?>
          </aside>
        </div>
      </section>

      <?php if (!empty($boutique_products)): ?>
      <section class="section ecosystem-shop" id="catalogue-boutique" aria-labelledby="ecosystem-shop-title">
        <div class="ecosystem-shop__inner">
          <header class="ecosystem-shop__head">
            <p class="section-eyebrow">Catalogue</p>
            <h2 id="ecosystem-shop-title" class="ecosystem-shop__title">Nos produits <?= e(mb_strtolower($service['short_label'])) ?></h2>
            <p class="ecosystem-shop__lead"><?= count($boutique_products) ?> références disponibles — commande en ligne, livraison suivie.</p>
          </header>
          <div class="ecosystem-shop__grid boutique-grid">
            <?php foreach ($boutique_products as $p):
              $meta = $product_categories[$p['category']] ?? ['label' => $p['category'], 'emoji' => '🛒']; ?>
            <article class="boutique-card">
              <a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="boutique-card__media<?= !empty($p['image']) ? ' boutique-card__media--photo' : '' ?>">
                <?= render_product_image($p, 'card') ?>
                <span class="boutique-card__cat"><?= e($meta['emoji']) ?> <?= e($meta['label']) ?></span>
              </a>
              <div class="boutique-card__body">
                <h3 class="boutique-card__title"><a href="<?= e(url('/produit/' . $p['slug'])) ?>"><?= e($p['name']) ?></a></h3>
                <?php if (!empty($p['weight_info'])): ?><p class="boutique-card__meta"><?= e($p['weight_info']) ?></p><?php endif; ?>
                <div class="boutique-card__footer">
                  <?= catalog_price_badge(price_euros($p)) ?>
                  <div class="boutique-card__actions">
                    <a href="<?= e(url('/produit/' . $p['slug'])) ?>" class="boutique-card__link">Fiche</a>
                    <form method="post" action="<?= e(url('/panier/ajouter')) ?>" class="boutique-card__form">
                      <?= csrf_field() ?>
                      <input type="hidden" name="product_id" value="<?= (int) $p['id'] ?>">
                      <input type="hidden" name="quantity" value="1">
                      <button type="submit" class="boutique-card__cart" title="Ajouter au panier" aria-label="Ajouter <?= e($p['name']) ?> au panier">+</button>
                    </form>
                  </div>
                </div>
              </div>
            </article>
            <?php endforeach; ?>
          </div>
          <div class="ecosystem-shop__cta">
            <a href="<?= e(url('/boutique?type=non-alimentaire&categorie=' . urlencode($service['boutique_category']))) ?>" class="btn-primary">Ouvrir la boutique <?= e(mb_strtolower($service['short_label'])) ?></a>
          </div>
        </div>
      </section>
      <?php endif; ?>

      <?php if ($has_form): require __DIR__ . '/ecosysteme/partials/demande_form.php'; endif; ?>
    </div>
  </div>
</div>
<?php if ($slides): ?>
<script>
(function(){var root=document.querySelector("[data-ecosystem-slideshow]");if(!root)return;var track=root.querySelector("[data-ecosystem-track]");var slides=root.querySelectorAll(".ecosystem-body__slide");if(!track||slides.length<2)return;var realCount=slides.length-1,interval=parseInt(root.getAttribute("data-interval")||"5000",10),index=0,moving=false,reduced=window.matchMedia("(prefers-reduced-motion: reduce)").matches;function setX(i,a){track.style.transition=(!a||reduced)?"none":"";track.style.transform="translate3d(-"+i*100+"%,0,0)";}track.addEventListener("transitionend",function(e){if(e.target!==track||e.propertyName!=="transform")return;if(index<realCount){moving=false;return;}setX(0,false);void track.offsetWidth;track.style.transition="";index=0;moving=false;});setInterval(function(){if(moving&&!reduced)return;moving=true;index+=1;setX(index,true);if(reduced&&index>=realCount){index=0;setX(0,false);moving=false;}},interval);})();
</script>
<?php endif; ?>
