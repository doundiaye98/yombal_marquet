<?php
/** Mega-menus Boutique + Univers YOMBAL (comme Flask macros/ecosystem_catbar.html) */
if ($isAdminEp) {
    return;
}
$alimentLabels = $shop_universe_labels['alimentaire'];
$nonAlimLabels = $shop_universe_labels['non-alimentaire'];
?>
<div id="mega-boutique" class="yombal-mega" role="region" aria-label="Boutique Yombal Marché" hidden>
  <div class="yombal-mega__panel">
    <div class="yombal-mega__cols">
      <div class="yombal-mega__col">
        <header class="yombal-mega__head">
          <span class="yombal-mega__badge"><?= e($alimentLabels['emoji']) ?></span>
          <div>
            <h3 class="yombal-mega__title"><?= e($alimentLabels['label']) ?></h3>
            <p class="yombal-mega__desc"><?= e($alimentLabels['description']) ?></p>
          </div>
        </header>
        <ul class="yombal-mega__links">
          <?php foreach ($shop_category_order as $key):
            if (in_array($key, $shop_non_alimentaire_rayons, true)) continue;
            $meta = $product_categories[$key] ?? ['label' => $key, 'emoji' => '🛒'];
          ?>
          <li>
            <a href="<?= e(url('/boutique?type=alimentaire&categorie=' . urlencode($key))) ?>">
              <span class="yombal-mega__link-emoji" aria-hidden="true"><?= e($meta['emoji']) ?></span>
              <span><?= e($meta['label']) ?></span>
            </a>
          </li>
          <?php endforeach; ?>
        </ul>
        <a href="<?= e(url('/boutique?type=alimentaire')) ?>" class="yombal-mega__all">Tout l'alimentaire →</a>
      </div>

      <div class="yombal-mega__col yombal-mega__col--accent">
        <header class="yombal-mega__head">
          <span class="yombal-mega__badge"><?= e($nonAlimLabels['emoji']) ?></span>
          <div>
            <h3 class="yombal-mega__title"><?= e($nonAlimLabels['label']) ?></h3>
            <p class="yombal-mega__desc"><?= e($nonAlimLabels['description']) ?></p>
          </div>
        </header>
        <ul class="yombal-mega__links">
          <?php foreach ($shop_non_alimentaire_rayons as $key):
            $meta = $product_categories[$key] ?? ['label' => $key, 'emoji' => '✨'];
          ?>
          <li>
            <a href="<?= e(url('/boutique?type=non-alimentaire&categorie=' . urlencode($key))) ?>">
              <span class="yombal-mega__link-emoji" aria-hidden="true"><?= e($meta['emoji']) ?></span>
              <span><?= e($meta['label']) ?></span>
            </a>
          </li>
          <?php endforeach; ?>
        </ul>
        <a href="<?= e(url('/boutique?type=non-alimentaire')) ?>" class="yombal-mega__all">Tout le non alimentaire →</a>
      </div>
    </div>

    <footer class="yombal-mega__foot">
      <a href="<?= e(url('/boutique')) ?>">Catalogue complet</a>
      <span class="yombal-mega__foot-sep" aria-hidden="true">·</span>
      <a href="<?= e(url('/panier')) ?>">Mon panier</a>
      <span class="yombal-mega__foot-sep" aria-hidden="true">·</span>
      <a href="<?= e(url('/recettes')) ?>">Paniers recettes</a>
    </footer>
  </div>
</div>

<div id="mega-univers" class="yombal-mega yombal-mega--univers" role="region" aria-label="Univers YOMBAL" hidden>
  <div class="yombal-mega__panel">
    <header class="yombal-mega__head yombal-mega__head--univers">
      <span class="yombal-mega__badge">✦</span>
      <div>
        <h3 class="yombal-mega__title">Univers YOMBAL</h3>
        <p class="yombal-mega__desc">Les services du Groupe YOMBAL — voyages, immobilier, investissement et plus.</p>
      </div>
    </header>
    <ul class="yombal-mega__links yombal-mega__links--ecosystem">
      <?php foreach ($ecosystem_nav as $item):
        $href = !empty($item['external_url']) ? $item['external_url'] : url('/ecosysteme/' . $item['slug']);
        $isActive = empty($item['external_url']) && $ep === 'ecosysteme_detail' && ($ecosystem_slug ?? '') === $item['slug'];
      ?>
      <li>
        <a
          href="<?= e($href) ?>"
          class="yombal-mega__eco-link<?= $isActive ? ' is-active' : '' ?>"
          <?php if (!empty($item['external_url'])): ?>target="_blank" rel="noopener noreferrer"<?php endif; ?>
          title="<?= e(($item['title'] ?? $item['short_label']) . (!empty($item['external_url']) ? ' (nouvel onglet)' : '')) ?>"
        >
          <span class="yombal-mega__link-emoji" aria-hidden="true"><?= e($item['icon']) ?></span>
          <span class="yombal-mega__eco-copy">
            <strong><?= e($item['short_label']) ?></strong>
            <small><?= e($item['tagline'] ?? '') ?></small>
          </span>
          <?php if (!empty($item['external_url'])): ?><span class="yombal-mega__eco-ext" aria-hidden="true">↗</span><?php endif; ?>
        </a>
      </li>
      <?php endforeach; ?>
    </ul>
    <footer class="yombal-mega__foot">
      <a href="<?= e(url('/contact')) ?>#agences">Nos agences</a>
      <span class="yombal-mega__foot-sep" aria-hidden="true">·</span>
      <a href="<?= e(url('/contact')) ?>">Contact</a>
      <span class="yombal-mega__foot-sep" aria-hidden="true">·</span>
      <a href="mailto:<?= e($shop_contact_email) ?>"><?= e($shop_contact_email) ?></a>
    </footer>
  </div>
</div>
