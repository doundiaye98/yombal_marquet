<?php
$immo_photo_slides = [
    'img/immobilier-btp.jpg',
    'img/yombal-immobilier-hero.jpg',
    'img/gallery-immo-villas.jpg',
    'img/gallery-immo-appartements.jpg',
    'img/gallery-immo-terrains.jpg',
    'img/gallery-immo-btp.jpg',
    'img/gallery-immo-renovation.jpg',
    'img/gallery-immo-etudes.jpg',
];
?>
<div class="page-wrapper immo-page">
  <header class="immo-hero" aria-labelledby="immo-hero-title">
    <div class="immo-hero__bg" aria-hidden="true">
      <img src="<?= e(asset('img/immobilier/gemini-terrain.png')) ?>" alt="">
      <div class="immo-hero__bg-shade"></div>
    </div>
    <div class="immo-hero__inner">
      <div class="immo-hero__copy">
        <p class="immo-hero__eyebrow">Groupe YOMBAL · <?= e($program['name']) ?></p>
        <h1 id="immo-hero-title" class="immo-hero__title"><?= e($service['title']) ?></h1>
        <p class="immo-hero__tagline"><?= e($program['tagline']) ?></p>
        <p class="immo-hero__lead"><?= e($program['intro']) ?></p>
        <div class="immo-hero__actions">
          <a href="<?= e(url('/ecosysteme/immobilier-btp/demande')) ?>" class="btn-primary">Demander un projet</a>
          <a href="#terrains" class="btn-outline immo-hero__btn-outline">Voir les terrains</a>
        </div>
      </div>
      <ul class="immo-hero__stats" aria-label="Points clés du programme">
        <li><strong>3</strong><span>Sites au Sénégal</span></li>
        <li><strong>150&nbsp;m²</strong><span>Par parcelle</span></li>
        <li><strong>0&nbsp;€</strong><span>Apport initial</span></li>
        <li><strong>30–48</strong><span>Mois de paiement</span></li>
      </ul>
    </div>
  </header>

  <div class="immo-body immo-body--photo">
    <div class="immo-body__bg immo-body__bg--slideshow" aria-hidden="true" data-immo-slideshow data-interval="5000">
      <div class="immo-body__track" data-immo-track>
        <?php foreach ($immo_photo_slides as $slide): ?>
        <div class="immo-body__slide" style="background-image: url('<?= e(asset($slide)) ?>')"></div>
        <?php endforeach; ?>
        <div class="immo-body__slide" style="background-image: url('<?= e(asset($immo_photo_slides[0])) ?>')"></div>
      </div>
    </div>
    <div class="immo-body__content">

  <nav class="immo-sites-nav" aria-label="Navigation des terrains">
    <div class="immo-sites-nav__inner">
      <?php foreach ($terrains as $i => $terrain): ?>
      <a href="#terrain-<?= e($terrain['slug']) ?>" class="immo-sites-nav__link<?= $i === 0 ? ' is-active' : '' ?>">
        <span class="immo-sites-nav__name"><?= e($terrain['location']) ?></span>
        <span class="immo-sites-nav__price"><?= e($terrain['price_label']) ?></span>
      </a>
      <?php endforeach; ?>
    </div>
  </nav>

  <section class="immo-terrains" id="terrains" aria-labelledby="immo-terrains-title">
    <header class="immo-section-head">
      <p class="section-eyebrow">Terrains à céder</p>
      <h2 id="immo-terrains-title" class="section-title">Choisissez votre <em>emplacement</em></h2>
      <p class="section-sub section-sub--tight">Paiement échelonné, accompagnement diaspora et protocole d'accord pour chaque site.</p>
    </header>

    <div class="immo-sites-list">
      <?php foreach ($terrains as $i => $terrain): ?>
      <article class="immo-site<?= ($i % 2 === 1) ? ' immo-site--alt' : '' ?>" id="terrain-<?= e($terrain['slug']) ?>">
        <div class="immo-site__card">
          <div class="immo-site__media">
            <figure class="immo-site__cover">
              <img src="<?= e(asset($terrain['cover'])) ?>" alt="<?= e($terrain['cover_alt']) ?>" width="960" height="640" loading="<?= $i === 0 ? 'eager' : 'lazy' ?>" decoding="async">
              <span class="immo-site__surface"><?= (int) $terrain['surface_m2'] ?>&nbsp;m²</span>
            </figure>
          </div>
          <div class="immo-site__panel">
            <header class="immo-site__header">
              <span class="immo-site__num" aria-hidden="true"><?= e(sprintf('%02d', $i + 1)) ?></span>
              <div class="immo-site__header-text">
                <p class="immo-site__eyebrow"><?= e($terrain['headline']) ?></p>
                <h3 class="immo-site__title"><?= e($terrain['location']) ?></h3>
                <p class="immo-site__loc"><span aria-hidden="true">📍</span> <?= e($terrain['country']) ?></p>
              </div>
            </header>
            <div class="immo-site__price-band">
              <div class="immo-site__price-main">
                <span class="immo-site__price-label">Prix total</span>
                <strong class="immo-site__price-value"><?= e($terrain['price_label']) ?></strong>
                <span class="immo-site__price-hint">Paiement échelonné · apport <?= e($terrain['deposit_label']) ?></span>
              </div>
              <dl class="immo-site__price-meta">
                <div><dt>Mensualité</dt><dd><?= e($terrain['monthly_label']) ?></dd></div>
                <div><dt>Durée</dt><dd><?= (int) $terrain['duration_months'] ?> mois</dd></div>
                <div><dt>Surface</dt><dd><?= (int) $terrain['surface_m2'] ?>&nbsp;m²</dd></div>
              </dl>
            </div>
            <dl class="immo-site__facts">
              <div class="immo-site__fact"><dt>Apport initial</dt><dd><?= e($terrain['deposit_label']) ?></dd></div>
              <div class="immo-site__fact"><dt>Nature juridique</dt><dd><?= e($terrain['legal_nature']) ?></dd></div>
              <div class="immo-site__fact"><dt>Modalité</dt><dd>Échelonné</dd></div>
            </dl>
            <?php if ($terrain['highlights']): ?>
            <ul class="immo-site__tags"><?php foreach ($terrain['highlights'] as $item): ?><li><?= e($item) ?></li><?php endforeach; ?></ul>
            <?php endif; ?>
            <div class="immo-site__includes">
              <h4>Accompagnement inclus</h4>
              <ul class="immo-site__checklist"><?php foreach ($terrain['services'] as $item): ?><li><?= e($item) ?></li><?php endforeach; ?></ul>
            </div>
            <div class="immo-site__actions">
              <a href="<?= e(url('/ecosysteme/immobilier-btp/demande?terrain=' . urlencode($terrain['slug']))) ?>" class="btn-primary immo-site__cta">Demander ce terrain</a>
              <a href="<?= e($contact['phone_href']) ?>" class="immo-site__phone"><?= e($contact['phone']) ?></a>
            </div>
          </div>
        </div>
      </article>
      <?php endforeach; ?>
    </div>
  </section>

  <section class="immo-btp-band" aria-labelledby="immo-btp-title">
    <div class="immo-btp-band__content">
      <p class="immo-btp-band__eyebrow">BTP · Groupe YOMBAL</p>
      <h2 id="immo-btp-title" class="immo-btp-band__title">Construction &amp; <em>rénovation</em></h2>
      <p class="immo-btp-band__lead">Du terrain à la maison livrée : gros œuvre, extensions, finitions et suivi de chantier pour concrétiser votre projet au Sénégal.</p>
      <ul class="immo-btp-band__list"><?php foreach ($service['bullets'] as $item): ?><li><?= e($item) ?></li><?php endforeach; ?></ul>
    </div>
  </section>

  <section class="immo-contact-band" aria-labelledby="immo-contact-title">
    <div class="immo-contact-band__inner">
      <div class="immo-contact-band__intro">
        <h2 id="immo-contact-title">Parlons de votre projet</h2>
        <p>Visite de site, protocole d'accord ou devis BTP — notre équipe vous répond rapidement.</p>
      </div>
      <div class="immo-contact-band__channels">
        <a href="<?= e($contact['phone_href']) ?>" class="immo-contact-band__channel"><span class="immo-contact-band__channel-label">Téléphone</span><strong><?= e($contact['phone']) ?></strong></a>
        <a href="mailto:<?= e($contact['email']) ?>" class="immo-contact-band__channel"><span class="immo-contact-band__channel-label">E-mail</span><strong><?= e($contact['email']) ?></strong></a>
        <div class="immo-contact-band__channel immo-contact-band__channel--static"><span class="immo-contact-band__channel-label">Adresse</span><strong><?= e($contact['address']) ?></strong></div>
      </div>
      <a href="<?= e(url('/ecosysteme/immobilier-btp/demande')) ?>" class="btn-primary immo-contact-band__form">Demander un projet</a>
    </div>
  </section>

    </div>
  </div>
</div>
<script>
(function () {
  var slideshow = document.querySelector("[data-immo-slideshow]");
  if (slideshow) {
    var track = slideshow.querySelector("[data-immo-track]");
    var slides = slideshow.querySelectorAll(".immo-body__slide");
    if (track && slides.length >= 2) {
      var realCount = slides.length - 1;
      var interval = parseInt(slideshow.getAttribute("data-interval") || "5000", 10);
      var index = 0, moving = false;
      var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      function setX(i, animate) { track.style.transition = !animate || reduced ? "none" : ""; track.style.transform = "translate3d(-" + i * 100 + "%, 0, 0)"; }
      track.addEventListener("transitionend", function (e) {
        if (e.target !== track || e.propertyName !== "transform") return;
        if (index < realCount) { moving = false; return; }
        setX(0, false); void track.offsetWidth; track.style.transition = ""; index = 0; moving = false;
      });
      setInterval(function () {
        if (moving && !reduced) return;
        moving = true; index += 1; setX(index, true);
        if (reduced && index >= realCount) { index = 0; setX(0, false); moving = false; }
      }, interval);
    }
  }
  var navLinks = document.querySelectorAll(".immo-sites-nav__link");
  var sections = document.querySelectorAll(".immo-site");
  if (navLinks.length && sections.length && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var id = entry.target.getAttribute("id");
        navLinks.forEach(function (link) {
          link.classList.toggle("is-active", link.getAttribute("href") === "#" + id);
        });
      });
    }, { rootMargin: "-40% 0px -50% 0px", threshold: 0 });
    sections.forEach(function (section) { observer.observe(section); });
  }
})();
</script>
