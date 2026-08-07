<?php
declare(strict_types=1);

try {
    require dirname(__DIR__) . '/app/bootstrap.php';
} catch (Throwable $e) {
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    $debug = (($_ENV['APP_DEBUG'] ?? getenv('APP_DEBUG')) === '1')
        || (isset($_GET['diag']) && $_GET['diag'] === '1');
    echo "Erreur serveur Yombal Market.\n";
    if ($debug) {
        echo $e->getMessage() . "\n" . $e->getFile() . ':' . $e->getLine() . "\n";
    } else {
        echo "Ajoutez ?diag=1 à l'URL ou ouvrez /diag.php pour le détail.\n";
    }
    exit;
}

$router = new Router();

$router->get('/', [ShopController::class, 'index']);
$router->get('/boutique', [ShopController::class, 'boutique']);
$router->get('/produit/{slug}', [ShopController::class, 'product']);

$router->get('/panier', [CartController::class, 'show']);
$router->post('/panier/ajouter', [CartController::class, 'add']);
$router->post('/panier/modifier', [CartController::class, 'update']);

$router->any('/auth/inscription', [AuthController::class, 'register']);
$router->any('/auth/connexion', [AuthController::class, 'login']);
$router->get('/auth/deconnexion', [AuthController::class, 'logout']);
$router->get('/compte', [AuthController::class, 'compte']);

$router->any('/checkout', [CheckoutController::class, 'checkout']);
$router->get('/paiement/{orderId}', [CheckoutController::class, 'paiement']);
$router->post('/paiement/{orderId}/manuel', [CheckoutController::class, 'paiementManuel']);
$router->post('/paiement/demo/{orderId}', [CheckoutController::class, 'paiementDemo']);

$router->any('/suivi-commande', [OrderController::class, 'suivi']);
$router->get('/suivi-commande/{orderId}', [OrderController::class, 'detail']);
$router->post('/commande/{orderId}/annuler', [OrderController::class, 'annuler']);
$router->post('/commande/{orderId}/recommander', [OrderController::class, 'recommander']);

$router->get('/apropos', [PageController::class, 'apropos']);
$router->any('/contact', [PageController::class, 'contact']);
$router->get('/services', [PageController::class, 'services']);
$router->get('/decouvrir', [PageController::class, 'decouvrir']);
$router->get('/saveurs', [PageController::class, 'saveurs']);
$router->get('/recettes', [PageController::class, 'recettes']);
$router->get('/recette/{slug}', [PageController::class, 'recette']);
$router->get('/coffrets', [PageController::class, 'coffrets']);
$router->get('/coffret/{slug}', [PageController::class, 'coffret']);
$router->any('/ecosysteme', [PageController::class, 'ecosystemeHub']);
$router->any('/ecosysteme/immobilier-btp/demande', [PageController::class, 'immoDemande']);
$router->any('/ecosysteme/{slug}', [PageController::class, 'ecosysteme']);
$router->post('/api/assistant', [PageController::class, 'apiAssistant']);
$router->get('/mentions-legales', [PageController::class, 'mentions']);
$router->get('/cgv', [PageController::class, 'cgv']);
$router->get('/healthz', [PageController::class, 'healthz']);
$router->get('/robots.txt', [PageController::class, 'robots']);
$router->get('/sitemap.xml', [PageController::class, 'sitemap']);
$router->get('/manifest.webmanifest', [PageController::class, 'manifest']);
$router->get('/sw.js', [PageController::class, 'sw']);

$router->any('/admin/connexion', [AdminController::class, 'login']);
$router->get('/admin/deconnexion', [AdminController::class, 'logout']);
$router->get('/admin/', [AdminController::class, 'dashboard']);
$router->get('/admin', [AdminController::class, 'dashboard']);
$router->get('/admin/produits', [AdminController::class, 'products']);
$router->any('/admin/produit/nouveau', fn () => AdminController::productForm(null));
$router->any('/admin/produit/{id}', [AdminController::class, 'productForm']);
$router->post('/admin/produit/{id}/supprimer', [AdminController::class, 'productDelete']);
$router->get('/admin/commandes', [AdminController::class, 'orders']);
$router->any('/admin/commande/{id}', [AdminController::class, 'orderDetail']);
$router->get('/admin/messages', [AdminController::class, 'messages']);
$router->post('/admin/message/{id}', [AdminController::class, 'messageRead']);

try {
    $router->dispatch(request_method(), $_SERVER['REQUEST_URI'] ?? '/');
} catch (Throwable $e) {
    http_response_code(500);
    header('Content-Type: text/plain; charset=utf-8');
    $debug = (config('debug') === true) || (isset($_GET['diag']) && $_GET['diag'] === '1');
    echo "Erreur serveur Yombal Market.\n";
    if ($debug) {
        echo $e->getMessage() . "\n" . $e->getFile() . ':' . $e->getLine() . "\n";
    } else {
        echo "Ajoutez ?diag=1 à l'URL ou ouvrez /diag.php pour le détail.\n";
    }
    exit;
}
