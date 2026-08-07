<?php
declare(strict_types=1);
$isAdminEp = str_starts_with((string) $ep, 'admin.');
$nav_shop = in_array($ep, ['boutique', 'product_detail', 'product_gamme', 'panier', 'checkout', 'paiement', 'suivi_commande', 'suivi_commande_detail'], true);
$nav_ecosystem = $ep === 'ecosysteme_detail';
$nav_discover = in_array($ep, ['decouvrir', 'saveurs', 'recettes', 'recette_detail', 'coffrets', 'coffret_detail'], true);
$tab_home = $ep === 'index';
$tab_cat = in_array($ep, ['boutique', 'product_detail', 'product_gamme'], true);
$tab_orders = in_array($ep, ['suivi_commande', 'suivi_commande_detail'], true);
$tab_contact = $ep === 'contact';
$tab_profile = in_array($ep, ['login', 'register', 'compte'], true);
?>
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="Yombal Marché — épicerie fine, cosmétiques, électronique et livraison à domicile. Boutique en ligne du Groupe YOMBAL.">
  <meta name="theme-color" content="#001858">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Yombal Market">
  <title><?= e($page_title) ?></title>
  <link rel="manifest" href="<?= e(url('/manifest.webmanifest')) ?>">
  <link rel="icon" href="<?= e(asset('img/yombal-logo.png')) ?>" type="image/png">
  <link rel="apple-touch-icon" href="<?= e(asset('img/icons/icon-180.png')) ?>">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Literata:ital,opsz,wght@0,7..72,400;0,7..72,600;0,7..72,700;0,7..72,800;1,7..72,400;1,7..72,600&family=Sora:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="<?= e(asset('css/style.css')) ?>">
  <link rel="stylesheet" href="<?= e(asset('css/modern.css')) ?>?v=23">
  <link rel="stylesheet" href="<?= e(asset('css/mobile.css')) ?>">
  <link rel="stylesheet" href="<?= e(asset('css/lusion.css')) ?>?v=13">
  <link rel="stylesheet" href="<?= e(asset('css/yombal-unified.css')) ?>?v=18">
  <link rel="stylesheet" href="<?= e(asset('css/catalog-label.css')) ?>?v=4">
  <link rel="stylesheet" href="<?= e(asset('css/ecosystem-nav.css')) ?>?v=5">
  <?= $extra_css ?>
</head>
<body class="<?= !$isAdminEp ? ' site-premium site-catalog-ud' : '' ?>">
  <a href="#main-content" class="skip-link">Aller au contenu</a>
  <div id="nav-backdrop" class="nav-backdrop" aria-hidden="true"></div>
  <div id="progress-bar" class="scroll-progress" aria-hidden="true"></div>
  <div id="cursor-dot" aria-hidden="true"></div>
  <div id="cursor-ring" aria-hidden="true"></div>
  <div id="grain" aria-hidden="true"></div>
  <div id="toast-root" class="toast-root" role="status" aria-live="polite"></div>

  <header class="site-header-unified<?= $isAdminEp ? ' site-header-unified--solo' : '' ?>" id="site-header" role="banner">
    <div class="header-shell">
      <a href="<?= e(url('/')) ?>" class="nav-logo" aria-label="Yombal Market — accueil">
        <img src="<?= e(asset('img/yombal-logo-nav.png')) ?>" alt="Yombal Market — Le goût du vrai, la fierté du local" class="nav-logo-img" width="180" height="60" decoding="async" onerror="this.onerror=null;this.src='<?= e(asset('img/icons/icon-180.png')) ?>';">
      </a>
      <ul id="primary-nav" class="nav-links" aria-label="Navigation principale">
        <li><a href="<?= e(url('/')) ?>" class="<?= $ep === 'index' ? 'active' : '' ?>">Accueil</a></li>
        <li><a href="<?= e(url('/apropos')) ?>" class="<?= $ep === 'apropos' ? 'active' : '' ?>">À propos</a></li>
        <li class="nav-item nav-item--mega">
          <button type="button" class="nav-mega-trigger<?= $nav_shop ? ' active' : '' ?>" data-mega="boutique" aria-expanded="false" aria-controls="mega-boutique" aria-haspopup="true">
            Boutique
            <svg class="nav-mega-chevron" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </li>
        <li class="nav-item nav-item--dropdown">
          <button type="button" class="nav-dropdown-trigger<?= $nav_discover ? ' active' : '' ?>" aria-expanded="false" aria-controls="nav-discover-menu" aria-haspopup="true">
            Découvrir <span class="nav-chevron" aria-hidden="true">▾</span>
          </button>
          <ul id="nav-discover-menu" class="nav-dropdown" role="menu">
            <li role="none"><a href="<?= e(url('/decouvrir')) ?>" role="menuitem" class="nav-dropdown-link<?= $ep === 'decouvrir' ? ' active' : '' ?>"><span class="nav-dropdown-icon" aria-hidden="true">✦</span> Vue d'ensemble</a></li>
            <li role="none"><a href="<?= e(url('/saveurs')) ?>" role="menuitem" class="nav-dropdown-link<?= $ep === 'saveurs' ? ' active' : '' ?>"><span class="nav-dropdown-icon" aria-hidden="true">🗺️</span> Carte des saveurs</a></li>
            <li role="none"><a href="<?= e(url('/recettes')) ?>" role="menuitem" class="nav-dropdown-link<?= in_array($ep, ['recettes', 'recette_detail'], true) ? ' active' : '' ?>"><span class="nav-dropdown-icon" aria-hidden="true">🍲</span> Recettes &amp; paniers</a></li>
            <li role="none"><a href="<?= e(url('/coffrets')) ?>" role="menuitem" class="nav-dropdown-link<?= in_array($ep, ['coffrets', 'coffret_detail'], true) ? ' active' : '' ?>"><span class="nav-dropdown-icon" aria-hidden="true">🎁</span> Coffrets cadeaux</a></li>
          </ul>
        </li>
        <?php if (!$isAdminEp): ?>
        <li class="nav-item nav-item--mega">
          <button type="button" class="nav-mega-trigger<?= $nav_ecosystem ? ' active' : '' ?>" data-mega="univers" aria-expanded="false" aria-controls="mega-univers" aria-haspopup="true">
            Univers YOMBAL
            <svg class="nav-mega-chevron" width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
          </button>
        </li>
        <?php endif; ?>
        <li><a href="<?= e(url('/suivi-commande')) ?>" class="<?= $tab_orders ? 'active' : '' ?>">Commandes</a></li>
        <li><a href="<?= e(url('/contact')) ?>" class="<?= $tab_contact ? 'active' : '' ?>">Contact</a></li>
        <?php if ($user): ?>
        <li><a href="<?= e(url('/compte')) ?>" class="<?= $tab_profile ? 'active' : '' ?>">Mon compte</a></li>
        <?php if ($is_shop_admin): ?><li><a href="<?= e(url('/admin/')) ?>" class="<?= $isAdminEp ? 'active' : '' ?>">Admin</a></li><?php endif; ?>
        <li><a href="<?= e(url('/auth/deconnexion')) ?>">Déconnexion</a></li>
        <?php else: ?>
        <li><a href="<?= e(url('/auth/connexion')) ?>" class="<?= $tab_profile ? 'active' : '' ?>">Espace client</a></li>
        <?php endif; ?>
      </ul>
      <div class="nav-actions">
        <a href="#pwa-install-sheet" id="pwa-install-btn" class="btn-pwa is-visible" aria-label="Installer l'application Yombal Market"><span class="btn-pwa__label">Installer l'app</span></a>
        <a href="<?= e(url('/panier')) ?>" class="nav-cart<?= in_array($ep, ['panier', 'checkout'], true) ? ' is-active' : '' ?>" aria-label="Panier<?= $cart_count ? ' — ' . $cart_count . ' articles' : '' ?>">
          <svg class="nav-cart__icon" width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6.5 7h14l-1.4 8.4a2 2 0 0 1-2 1.6H9.2a2 2 0 0 1-2-1.7L5.4 3.5H3" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><circle cx="10" cy="20" r="1.4" fill="currentColor"/><circle cx="17.5" cy="20" r="1.4" fill="currentColor"/></svg>
          <?php if ($cart_count): ?><span class="nav-cart__badge"><?= (int) $cart_count ?></span><?php endif; ?>
        </a>
        <a href="<?= e(url('/boutique')) ?>" class="btn-nav">Commander</a>
      </div>
      <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="cine-nav" aria-label="Ouvrir le menu"><span class="nav-toggle__icon" aria-hidden="true"></span><span class="nav-toggle__label">Menu</span></button>
    </div>
    <?php require __DIR__ . '/partials/mega_menus.php'; ?>
  </header>

  <nav id="cine-nav" class="cine-nav" aria-label="Navigation principale" aria-hidden="true">
    <div class="cine-nav__backdrop" data-cine-close aria-hidden="true"></div>
    <div class="cine-nav__panel">
      <div class="cine-nav__glow" aria-hidden="true"></div>
      <button type="button" class="cine-nav__close" data-cine-close aria-label="Fermer le menu">×</button>
      <p class="cine-nav__eyebrow">Yombal Marché · Groupe YOMBAL</p>
      <ul class="cine-nav__links">
        <li><a href="<?= e(url('/')) ?>" class="cine-nav__link<?= $ep === 'index' ? ' is-active' : '' ?>"><span class="cine-nav__num">01</span><span class="cine-nav__text">Accueil</span></a></li>
        <li><a href="<?= e(url('/apropos')) ?>" class="cine-nav__link<?= $ep === 'apropos' ? ' is-active' : '' ?>"><span class="cine-nav__num">02</span><span class="cine-nav__text">À propos</span></a></li>
        <li><a href="<?= e(url('/boutique')) ?>" class="cine-nav__link<?= $nav_shop ? ' is-active' : '' ?>"><span class="cine-nav__num">03</span><span class="cine-nav__text">Boutique</span></a></li>
        <li><a href="<?= e(url('/decouvrir')) ?>" class="cine-nav__link<?= $ep === 'decouvrir' ? ' is-active' : '' ?>"><span class="cine-nav__num">04</span><span class="cine-nav__text">Découvrir</span></a></li>
        <li><a href="<?= e(url('/saveurs')) ?>" class="cine-nav__link<?= $ep === 'saveurs' ? ' is-active' : '' ?>"><span class="cine-nav__num">05</span><span class="cine-nav__text">Carte des saveurs</span></a></li>
        <li><a href="<?= e(url('/recettes')) ?>" class="cine-nav__link<?= in_array($ep, ['recettes', 'recette_detail'], true) ? ' is-active' : '' ?>"><span class="cine-nav__num">06</span><span class="cine-nav__text">Recettes</span></a></li>
        <li><a href="<?= e(url('/coffrets')) ?>" class="cine-nav__link<?= in_array($ep, ['coffrets', 'coffret_detail'], true) ? ' is-active' : '' ?>"><span class="cine-nav__num">07</span><span class="cine-nav__text">Coffrets</span></a></li>
        <li><a href="<?= e(url('/panier')) ?>" class="cine-nav__link<?= in_array($ep, ['panier', 'checkout'], true) ? ' is-active' : '' ?>"><span class="cine-nav__num">08</span><span class="cine-nav__text">Panier<?= $cart_count ? ' <em class="cine-nav__badge">' . (int) $cart_count . '</em>' : '' ?></span></a></li>
        <li><a href="<?= e(url('/suivi-commande')) ?>" class="cine-nav__link<?= $tab_orders ? ' is-active' : '' ?>"><span class="cine-nav__num">09</span><span class="cine-nav__text">Commandes</span></a></li>
        <li class="cine-nav__divider" role="separator"><span>Univers YOMBAL</span></li>
        <?php foreach ($ecosystem_nav as $idx => $item): ?>
        <li><a href="<?= e($item['external_url'] ?: url('/ecosysteme/' . $item['slug'])) ?>" class="cine-nav__link"><span class="cine-nav__num"><?= e(sprintf('%02d', $idx + 10)) ?></span><span class="cine-nav__text"><?= e($item['icon']) ?> <?= e($item['short_label']) ?></span></a></li>
        <?php endforeach; ?>
      </ul>
      <div class="cine-nav__foot">
        <a href="#pwa-install-sheet" class="btn-pwa cine-nav__pwa is-visible" id="pwa-install-btn-mobile">Installer l'app</a>
        <a href="<?= e(url('/boutique')) ?>" class="xd-btn xd-btn--light">Commander maintenant</a>
        <a href="mailto:<?= e($shop_contact_email) ?>" class="cine-nav__email"><?= e($shop_contact_email) ?></a>
      </div>
    </div>
  </nav>

  <?php if (!$isAdminEp): ?>
  <nav class="m-tabbar" aria-label="Navigation rapide mobile">
    <a href="<?= e(url('/')) ?>" class="m-tabbar__item<?= $tab_home ? ' is-active' : '' ?>">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4 10.5 12 4l8 6.5V20a1 1 0 0 1-1 1h-5v-6H10v6H5a1 1 0 0 1-1-1v-9.5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></svg>
      <span class="m-tabbar__label">Accueil</span>
    </a>
    <a href="<?= e(url('/boutique')) ?>" class="m-tabbar__item<?= $tab_cat ? ' is-active' : '' ?>">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="3.5" y="3.5" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.7"/><rect x="13.5" y="3.5" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.7"/><rect x="3.5" y="13.5" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.7"/><rect x="13.5" y="13.5" width="7" height="7" rx="1.5" stroke="currentColor" stroke-width="1.7"/></svg>
      <span class="m-tabbar__label">Catégories</span>
    </a>
    <a href="<?= e(url('/suivi-commande')) ?>" class="m-tabbar__item<?= $tab_orders ? ' is-active' : '' ?>">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M8 7h11a1 1 0 0 1 1 1v11a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1V8a1 1 0 0 1 1-1Z" stroke="currentColor" stroke-width="1.7"/><path d="M7 17H5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h11a1 1 0 0 1 1 1v2" stroke="currentColor" stroke-width="1.7"/><path d="M10.5 12h6M10.5 15.5h4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
      <span class="m-tabbar__label">Commandes</span>
    </a>
    <a href="<?= e(url('/contact')) ?>" class="m-tabbar__item<?= $tab_contact ? ' is-active' : '' ?>">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M4.5 7.5h15v10a1.5 1.5 0 0 1-1.5 1.5h-12A1.5 1.5 0 0 1 4.5 17.5v-10Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="m5 8 7 5.5L19 8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <span class="m-tabbar__label">Contact</span>
    </a>
    <a href="<?= e(url($user ? '/compte' : '/auth/connexion')) ?>" class="m-tabbar__item<?= $tab_profile ? ' is-active' : '' ?>">
      <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="8" r="3.25" stroke="currentColor" stroke-width="1.7"/><path d="M5.5 19.5c1.6-3.2 4-4.8 6.5-4.8s4.9 1.6 6.5 4.8" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
      <span class="m-tabbar__label">Profil</span>
    </a>
  </nav>
  <?php endif; ?>

  <main id="main-content" class="site-main <?= e($main_class) ?>">
    <?php if ($flashes): ?><div class="flash-stack" role="alert"><?php foreach ($flashes as $f): ?><div class="flash flash-<?= e($f['cat']) ?>"><?= e($f['msg']) ?></div><?php endforeach; ?></div><?php endif; ?>
    <?php require $view_file; ?>
  </main>

  <footer class="site-footer">
    <div class="footer-inner footer-grid">
      <div class="footer-col">
        <a href="<?= e(url('/')) ?>" class="footer-logo-link"><img src="<?= e(asset('img/yombal-logo.png')) ?>" alt="Yombal Market" class="footer-logo-img" width="180" height="54" loading="lazy" decoding="async"></a>
        <p class="footer-tagline">Produits alimentaires et cosmétiques, livraison à domicile et boutique en ligne — une enseigne du <strong>Groupe YOMBAL</strong>.</p>
        <div class="footer-email-block"><span class="footer-email-label">Contact</span><a href="mailto:<?= e($shop_contact_email) ?>" class="email-chip email-chip--footer"><span class="email-chip-text"><?= e($shop_contact_email) ?></span></a></div>
      </div>
      <nav class="footer-col" aria-label="Navigation boutique">
        <h3>Boutique</h3>
        <a href="<?= e(url('/boutique')) ?>">Catalogue</a><a href="<?= e(url('/boutique?type=alimentaire')) ?>">Alimentaires</a><a href="<?= e(url('/boutique?type=non-alimentaire')) ?>">Non alimentaires</a><a href="<?= e(url('/boutique?categorie=cosmetique')) ?>">Cosmétique</a><a href="<?= e(url('/boutique?categorie=electronique')) ?>">Électronique</a><a href="<?= e(url('/boutique?categorie=electromenager')) ?>">Électroménager</a><a href="<?= e(url('/boutique?categorie=mode')) ?>">Habillement</a><a href="<?= e(url('/boutique?categorie=chaussures')) ?>">Chaussures</a><a href="<?= e(url('/boutique?categorie=bagagerie')) ?>">Sacs & bagagerie</a><a href="<?= e(url('/boutique?categorie=poisson')) ?>">Produits de la mer</a><a href="<?= e(url('/decouvrir')) ?>">Découvrir l'expérience</a><a href="<?= e(url('/saveurs')) ?>">Carte des saveurs</a><a href="<?= e(url('/recettes')) ?>">Recettes & paniers</a><a href="<?= e(url('/coffrets')) ?>">Coffrets cadeaux</a><a href="<?= e(url('/panier')) ?>">Mon panier</a><a href="<?= e(url('/checkout')) ?>">Commander</a><a href="<?= e(url('/suivi-commande')) ?>">Suivi de commande</a>
      </nav>
      <nav class="footer-col" aria-label="Informations">
        <h3>Informations</h3>
        <a href="<?= e(url('/services')) ?>">Services</a><a href="<?= e(url('/ecosysteme')) ?>">Univers YOMBAL</a><a href="<?= e(url('/ecosysteme/immobilier-btp')) ?>">Immobilier & BTP</a><a href="<?= e(url('/ecosysteme/electronique')) ?>">Électronique</a><a href="<?= e(url('/ecosysteme/electromenager')) ?>">Électroménager</a><a href="<?= e(url('/ecosysteme/mode')) ?>">Habillement</a><a href="<?= e(url('/ecosysteme/chaussures')) ?>">Chaussures</a><a href="<?= e(url('/ecosysteme/bagagerie')) ?>">Sacs & bagagerie</a><a href="<?= e(url('/apropos')) ?>">À propos</a><a href="<?= e(url('/contact')) ?>">Contact & paiement</a><a href="<?= e(url('/mentions-legales')) ?>">Mentions légales</a><a href="<?= e(url('/mentions-legales#cookies')) ?>">Cookies</a><a href="<?= e(url('/cgv')) ?>">CGV</a>
      </nav>
    </div>
    <div class="footer-bottom"><p class="footer-copy">© <?= $current_year ?> Yombal Marché · Groupe YOMBAL</p><span class="footer-badge">Responsive · Sécurisé</span></div>
  </footer>

  <div id="cookie-consent" class="cookie-consent" role="dialog" aria-labelledby="cookie-consent-title" aria-hidden="true" hidden><div class="cookie-consent-inner"><p id="cookie-consent-title" class="cookie-consent-title">Cookies & confidentialité</p><p class="cookie-consent-text">Nous utilisons des cookies essentiels (panier, session) pour le fonctionnement de la boutique. Consultez nos <a href="<?= e(url('/mentions-legales#cookies')) ?>">mentions légales</a>.</p><button type="button" class="btn-primary cookie-consent-btn" data-cookie-accept>OK, j'ai compris</button></div></div>

  <?php if (!empty($assistant_enabled)): ?>
  <div id="assistant-widget" class="assistant-widget" data-ready="<?= !empty($assistant_ready) ? '1' : '0' ?>" data-api-url="<?= e(url('/api/assistant')) ?>" data-suivi-url="<?= e(url('/suivi-commande')) ?>">
    <button type="button" id="assistant-fab" class="assistant-fab" aria-expanded="false" aria-controls="assistant-panel" aria-label="Ouvrir le conseiller Yombal Market">
      <span class="assistant-fab-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M4 12a8 8 0 0 1 8-8h0a8 8 0 0 1 8 8v5.2A2.8 2.8 0 0 1 17.2 20H12a8 8 0 0 1-8-8Z" stroke="currentColor" stroke-width="1.8"/><path d="M9 11.5h6M9 14.5h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
      </span>
    </button>
    <section id="assistant-panel" class="assistant-panel" role="dialog" aria-labelledby="assistant-title" aria-hidden="true">
      <header class="assistant-header">
        <div class="assistant-header-brand">
          <img class="assistant-header-logo" src="<?= e(asset('img/yombal-logo.png')) ?>" alt="" width="40" height="40" decoding="async">
          <div class="assistant-header-text">
            <h2 id="assistant-title">Conseiller Yombal Market</h2>
            <p>Service client</p>
            <span class="assistant-status">Disponible</span>
          </div>
        </div>
        <button type="button" id="assistant-close" class="assistant-close" aria-label="Fermer le conseiller">×</button>
      </header>
      <div id="assistant-messages" class="assistant-messages" aria-live="polite" aria-relevant="additions"></div>
      <div id="assistant-chips" class="assistant-chips" aria-label="Questions fréquentes" hidden></div>
      <form id="assistant-form" class="assistant-form">
        <label for="assistant-input" class="sr-only">Votre question</label>
        <input id="assistant-input" class="assistant-input" type="text" name="question" maxlength="500" placeholder="Votre langue : FR, EN, wolof…" autocomplete="off" required>
        <button type="submit" class="assistant-send">Envoyer</button>
      </form>
    </section>
  </div>
  <link rel="stylesheet" href="<?= e(asset('css/assistant.css')) ?>">
  <script src="<?= e(asset('js/assistant-widget.js')) ?>?v=2" defer></script>
  <?php endif; ?>

  <div id="pwa-install-sheet" class="pwa-ios-hint" role="dialog" aria-modal="true" aria-labelledby="pwa-ios-title"><div class="pwa-ios-hint__card"><a href="#" class="pwa-ios-hint__close" id="pwa-ios-close" aria-label="Fermer">×</a><p id="pwa-ios-title" class="pwa-ios-hint__title">Installer Yombal Market</p><p id="pwa-ios-text" class="pwa-ios-hint__text"><strong>Sur iPhone (Safari)</strong><br>1. Appuyez sur <strong>Partager</strong> <span aria-hidden="true">□↑</span> en bas de l'écran.<br>2. Choisissez <strong>« Sur l'écran d'accueil »</strong>.<br>3. Validez avec <strong>Ajouter</strong>.</p><a href="#" class="pwa-ios-hint__ok" id="pwa-ios-ok">J'ai compris</a></div></div>
  <script src="<?= e(asset('js/cookie-consent.js')) ?>" defer></script>
  <script src="<?= e(asset('js/site-experience.js')) ?>?v=2" defer></script>
  <script src="<?= e(asset('js/animations.js')) ?>" defer></script>
  <script src="<?= e(asset('js/ecosystem-nav.js')) ?>" defer></script>
  <script src="<?= e(asset('js/pwa-install.js')) ?>?v=4" defer></script>
  <?= $extra_scripts ?>
</body>
</html>
