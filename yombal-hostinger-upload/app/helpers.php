<?php
declare(strict_types=1);

function e(?string $s): string { return htmlspecialchars((string) $s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); }
function env(string $key, ?string $default = null): ?string { $v = $_ENV[$key] ?? getenv($key); return ($v === false || $v === null || $v === '') ? $default : (string) $v; }
function config(string $key, mixed $default = null): mixed { return $GLOBALS['app_config'][$key] ?? $default; }
function url(string $path = ''): string { $base = rtrim((string) config('app_url', ''), '/'); $path = '/' . ltrim($path, '/'); return $path === '/' ? ($base ?: '/') : (($base ?: '') . $path); }
function asset(string $path): string { return url('static/' . ltrim($path, '/')); }
function redirect(string $path): never { header('Location: ' . (str_starts_with($path, 'http') ? $path : url($path))); exit; }
function flash(string $message, string $category = 'info'): void { $_SESSION['_flashes'][] = ['cat' => $category, 'msg' => $message]; }
function get_flashes(): array { $f = $_SESSION['_flashes'] ?? []; unset($_SESSION['_flashes']); return $f; }
function money_eur(int $cents): string { return number_format($cents / 100, 2, '.', '') . ' €'; }
function price_euros(array $product): float { return ((int) ($product['price_cents'] ?? 0)) / 100; }
function csrf_token(): string { if (empty($_SESSION['_csrf'])) $_SESSION['_csrf'] = bin2hex(random_bytes(32)); return $_SESSION['_csrf']; }
function csrf_field(): string { return '<input type="hidden" name="_csrf" value="' . e(csrf_token()) . '">'; }
function verify_csrf(): void { $t = $_POST['_csrf'] ?? ''; if (!$t || !hash_equals($_SESSION['_csrf'] ?? '', $t)) { http_response_code(403); exit('Jeton CSRF invalide.'); } }
function request_method(): string { return strtoupper($_SERVER['REQUEST_METHOD'] ?? 'GET'); }
function is_post(): bool { return request_method() === 'POST'; }
function product_categories(): array { return [
    'cereales'=>['label'=>'Céréales','emoji'=>'🌾'],'legumineuses'=>['label'=>'Légumineuses','emoji'=>'🫘'],'huiles'=>['label'=>'Huiles & graisses','emoji'=>'🫒'],
    'snacks'=>['label'=>'Snacks','emoji'=>'🥨'],'desserts'=>['label'=>'Desserts','emoji'=>'🍮'],'boissons'=>['label'=>'Boissons & sirops','emoji'=>'🥤'],
    'condiments'=>['label'=>'Condiments','emoji'=>'🧂'],'fruits'=>['label'=>'Fruits','emoji'=>'🍊'],'legumes'=>['label'=>'Légumes','emoji'=>'🥬'],
    'conserves'=>['label'=>'Conserves','emoji'=>'🫙'],'poisson'=>['label'=>'Produits de la mer','emoji'=>'🐟'],'viandes'=>['label'=>'Viandes & volailles','emoji'=>'🍗'],
    'cosmetique'=>['label'=>'Cosmétique','emoji'=>'✨'],'electronique'=>['label'=>'Électronique','emoji'=>'📱'],'electromenager'=>['label'=>'Électroménager','emoji'=>'🏠'],
    'mode'=>['label'=>'Habillement','emoji'=>'👕'],'chaussures'=>['label'=>'Chaussures','emoji'=>'👟'],'bagagerie'=>['label'=>'Sacs & bagagerie','emoji'=>'🎒'],
    'miels'=>['label'=>'Miels & confitures','emoji'=>'🍯'],'epices'=>['label'=>'Épices','emoji'=>'🌶️'],
]; }
function category_labels(): array { return array_map(fn($m) => $m['label'], product_categories()); }
function product_image_url(?string $image): string { if (!$image) return asset('img/icons/icon-180.png'); return (str_starts_with($image, 'http://') || str_starts_with($image, 'https://')) ? $image : asset(ltrim($image, '/')); }
function render_product_image(array $product, string $variant = 'card'): string { if (!empty($product['image'])) return '<img src="' . e(product_image_url($product['image'])) . '" alt="' . e($product['name'] ?? '') . '" class="product-photo product-photo--' . e($variant) . '" loading="lazy" decoding="async">'; $meta = product_categories()[$product['category'] ?? ''] ?? ['emoji' => '🛒']; return '<span class="product-photo-fallback" aria-hidden="true">' . e($product['icon'] ?? $meta['emoji']) . '</span>'; }
function catalog_price_badge(float $price): string { return '<span class="catalog-price-badge boutique-card__price" aria-label="Prix ' . e(number_format($price, 2, '.', '')) . ' euros"><span class="catalog-price-badge__amount">' . e(number_format($price, 2, '.', '')) . ' €</span><span class="catalog-price-badge__label">Prix</span></span>'; }
function ecosystem_nav_items(): array {
    return [
        ['slug'=>'voyages','icon'=>'✈️','short_label'=>'Voyages','tagline'=>'Agence de voyages TourCom','external_url'=>'https://www.terangavoyages.com/'],
        ['slug'=>'investissement','icon'=>'📈','short_label'=>'Investissement','tagline'=>'Opportunités d\'investissement et projets','external_url'=>null],
        ['slug'=>'immobilier-btp','icon'=>'🏗️','short_label'=>'Immobilier & BTP','tagline'=>'Programme YOMBAL KEUR — terrains diaspora & construction','external_url'=>null],
        ['slug'=>'transport','icon'=>'🚗','short_label'=>'Transports','tagline'=>'Véhicules, location, déménagement et colis','external_url'=>null],
        ['slug'=>'restaurant','icon'=>'🍽️','short_label'=>'Restaurant','tagline'=>'Restauration et saveurs africaines','external_url'=>null],
        ['slug'=>'electronique','icon'=>'📱','short_label'=>'Électronique','tagline'=>'Smartphones, high-tech et accessoires','external_url'=>null],
        ['slug'=>'electromenager','icon'=>'🏠','short_label'=>'Électroménager','tagline'=>'Petit électroménager du quotidien','external_url'=>null],
        ['slug'=>'mode','icon'=>'👗','short_label'=>'Habillement','tagline'=>'Mode et pièces diaspora','external_url'=>null],
        ['slug'=>'chaussures','icon'=>'👟','short_label'=>'Chaussures','tagline'=>'Baskets, sandales, ville et enfants','external_url'=>null],
        ['slug'=>'bagagerie','icon'=>'🧳','short_label'=>'Sacs & bagagerie','tagline'=>'Sacs, valises et voyage','external_url'=>null],
        ['slug'=>'coiffure','icon'=>'💇','short_label'=>'Coiffure','tagline'=>'Coiffure afro et soins capillaires','external_url'=>null],
    ];
}
function ecosystem_hub_services(): array { return ecosystem_nav_items(); }
function shop_alimentaire_rayons(): array {
    return ['miels','boissons','cereales','legumineuses','huiles','condiments','fruits','legumes','snacks','desserts','conserves','poisson','viandes','epices'];
}
function shop_non_alimentaire_rayons(): array {
    return ['cosmetique','electronique','electromenager','mode','chaussures','bagagerie'];
}
function shop_category_order(): array {
    return array_merge(shop_alimentaire_rayons(), shop_non_alimentaire_rayons());
}
function shop_universe_labels(): array {
    return [
        'alimentaire' => [
            'label' => 'Alimentaires',
            'emoji' => '🛒',
            'description' => 'Riz, épices, fruits, légumes, produits de la mer et épicerie fine.',
        ],
        'non-alimentaire' => [
            'label' => 'Non alimentaires',
            'emoji' => '✨',
            'description' => 'Électronique, électroménager, mode, chaussures, sacs et cosmétique.',
        ],
    ];
}
function shop_settings(): array { return ['shop_delivery_days_min' => '3', 'shop_delivery_days_max' => '7']; }
function checkout_delivery_estimate(): array { return ['label' => '3 à 7 jours ouvrés', 'days_min' => 3, 'days_max' => 7]; }
function order_status_label(string $status): string { return ['pending'=>'En attente de paiement','awaiting_wire'=>'Virement en cours','awaiting_paypal'=>'PayPal en attente','cod_confirmed'=>'Paiement à la livraison','paid_stripe'=>'Payée — en préparation','paid_demo'=>'Payée — en préparation','paid_manual'=>'Payée — en préparation','shipped'=>'Expédiée','cancelled'=>'Annulée'][$status] ?? $status; }
function checkout_steps(string $active): string { $cart = $active === 'cart' ? 'is-active' : (in_array($active, ['checkout','payment','done'], true) ? 'is-done' : ''); $checkout = $active === 'checkout' ? 'is-active' : (in_array($active, ['payment','done'], true) ? 'is-done' : ''); $payment = $active === 'payment' ? 'is-active' : ($active === 'done' ? 'is-done' : ''); return '<nav class="checkout-steps" aria-label="Étapes de commande"><a href="' . e(url('/panier')) . '" class="checkout-step ' . $cart . '"><span class="checkout-step-num">1</span><span class="checkout-step-label">Panier</span></a><span class="checkout-step-line" aria-hidden="true"></span><a href="' . e($active !== 'cart' ? url('/checkout') : '#') . '" class="checkout-step ' . $checkout . '"><span class="checkout-step-num">2</span><span class="checkout-step-label">Coordonnées</span></a><span class="checkout-step-line" aria-hidden="true"></span><span class="checkout-step ' . $payment . '"><span class="checkout-step-num">3</span><span class="checkout-step-label">Paiement</span></span></nav>'; }
function order_trust_panel(string $variant='full'): string { $shop = shop_settings(); $est = checkout_delivery_estimate(); $email = env('CONTACT_EMAIL', 'compta@universdiasporas.com'); return '<aside class="order-trust order-trust--' . e($variant) . ' reveal" aria-label="Acheter en confiance"><header class="order-trust__head"><h2 class="order-trust__title">Acheter en confiance</h2><p class="order-trust__lead">Commandez tranquillement — infos claires avant le paiement.</p></header><ul class="order-trust__grid"><li class="order-trust__item"><span class="order-trust__icon" aria-hidden="true">👤</span><div><strong>Sans compte obligatoire</strong><p>Indiquez vos coordonnées à la commande. Pas besoin de créer un compte.</p></div></li><li class="order-trust__item"><span class="order-trust__icon" aria-hidden="true">🚚</span><div><strong>Livraison ' . e($shop['shop_delivery_days_min']) . '–' . e($shop['shop_delivery_days_max']) . ' j. ouvrés</strong><p>Estimation typique : <strong>' . e($est['label']) . '</strong>.</p></div></li><li class="order-trust__item"><span class="order-trust__icon" aria-hidden="true">💳</span><div><strong>Modes de paiement</strong><p>Carte bancaire (Stripe) · PayPal · Virement · Espèces à la livraison.</p></div></li><li class="order-trust__item order-trust__item--contact"><span class="order-trust__icon" aria-hidden="true">💬</span><div><strong>Une question ?</strong><p><a href="mailto:' . e($email) . '">' . e($email) . '</a> · <a href="' . e(url('/contact')) . '">Formulaire contact</a> · <a href="' . e(url('/suivi-commande')) . '">Suivi commande</a></p></div></li></ul></aside>'; }
function view(string $name, array $data = []): void { extract($data, EXTR_SKIP); $flashes = get_flashes(); $ep = $data['ep'] ?? $name; $cart_count = Cart::count(); $user = Auth::user(); $is_shop_admin = Auth::isAdmin(); $shop_contact_email = env('CONTACT_EMAIL', 'compta@universdiasporas.com'); $current_year = (int) date('Y'); $ecosystem_nav = ecosystem_nav_items(); $shop_type_alimentaire = 'alimentaire'; $shop_type_non_alimentaire = 'non-alimentaire'; $shop_universe_labels = shop_universe_labels(); $shop_non_alimentaire_rayons = shop_non_alimentaire_rayons(); $shop_category_order = shop_category_order(); $ecosystem_slug = null; if (preg_match('~/ecosysteme/([^/?#]+)~', (string) ($_SERVER['REQUEST_URI'] ?? ''), $m)) { $ecosystem_slug = rawurldecode($m[1]); } $main_class = $data['main_class'] ?? ''; $page_title = $data['page_title'] ?? 'Yombal Market'; $extra_css = $data['extra_css'] ?? ''; $extra_scripts = $data['extra_scripts'] ?? ''; $product_categories = product_categories(); $shop_settings = shop_settings(); $assistant_enabled = Assistant::enabled() && !str_starts_with((string) $ep, 'admin.'); $assistant_ready = Assistant::ready(); $view_file = dirname(__DIR__) . '/views/' . $name . '.php'; if (!is_file($view_file)) { http_response_code(500); exit('Vue introuvable: ' . e($name)); } require dirname(__DIR__) . '/views/layout.php'; }
