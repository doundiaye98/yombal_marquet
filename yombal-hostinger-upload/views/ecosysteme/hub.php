<?php
/** Hub Univers YOMBAL */
$hub = $hub_services ?? [];
?>
<div class="page-wrapper ecosystem-page">
  <header class="ecosystem-hero ecosystem-hero--autres-services">
    <div class="ecosystem-hero__inner">
      <span class="ecosystem-hero__icon" aria-hidden="true">✦</span>
      <p class="ecosystem-hero__eyebrow">Groupe YOMBAL</p>
      <h1 class="ecosystem-hero__title">Univers YOMBAL</h1>
      <p class="ecosystem-hero__tagline">Tous nos services, une seule exigence de qualité</p>
      <p class="ecosystem-hero__lead">Boutique, immobilier &amp; BTP, électronique, mode, voyages et plus — choisissez le service qui vous concerne.</p>
    </div>
  </header>

  <section class="section ecosystem-hub">
    <div class="ecosystem-hub__inner">
      <p class="section-eyebrow">Groupe YOMBAL</p>
      <h2 class="ecosystem-hub__title">Tous nos services</h2>
      <p class="ecosystem-hub__lead">Une demande, une équipe — explorez chaque univers du groupe.</p>
      <div class="ecosystem-hub__grid">
        <?php foreach ($hub as $item): ?>
        <article class="ecosystem-hub__card">
          <span class="ecosystem-hub__icon" aria-hidden="true"><?= e($item['icon']) ?></span>
          <h3><?= e($item['short_label']) ?></h3>
          <p><?= e($item['tagline']) ?></p>
          <?php if (!empty($item['external_url'])): ?>
          <a href="<?= e($item['external_url']) ?>" class="ecosystem-hub__link" target="_blank" rel="noopener noreferrer">Découvrir ↗</a>
          <?php else: ?>
          <a href="<?= e(url('/ecosysteme/' . $item['slug'])) ?>" class="ecosystem-hub__link">
            <?= $item['slug'] === 'immobilier-btp' ? 'Voir le programme' : 'En savoir plus' ?>
          </a>
          <?php endif; ?>
        </article>
        <?php endforeach; ?>
      </div>
    </div>
  </section>
</div>
