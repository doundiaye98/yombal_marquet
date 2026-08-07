<?php
/**
 * Installation one-shot Hostinger — À SUPPRIMER après succès.
 *
 * 1) Uploadez ce fichier dans public_html/ (à côté de index.php)
 * 2) Ouvrez https://yombalmarket.com/fix.php
 * 3) Supprimez fix.php dès que c’est OK
 */
declare(strict_types=1);

header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex');
ini_set('display_errors', '1');
error_reporting(E_ALL);

$phpRoot = __DIR__ . '/php';
if (!is_dir($phpRoot . '/app')) {
    $phpRoot = __DIR__; // structure alternative : app/ à la racine web
}
if (!is_dir($phpRoot . '/app')) {
    http_response_code(500);
    echo '<h1>Dossier php/app introuvable</h1><p>Attendu : public_html/php/app/</p><pre>'
        . htmlspecialchars(__DIR__) . '</pre>';
    exit;
}

$envPath = $phpRoot . '/.env';
$secret = bin2hex(random_bytes(24));

$candidates = [
    ['name' => 'u528552725_ymk', 'user' => 'u528552725_ymk'],
    ['name' => 'u528552725_yombal', 'user' => 'u528552725_ymk'],
    ['name' => 'u528552725_ymk', 'user' => 'u528552725_ud'],
    ['name' => 'u528552725_yombal', 'user' => 'u528552725_ud'],
];
$pass = 'UdBase2026!Paris';
$host = 'localhost';
$port = '3306';

$working = null;
$errors = [];
foreach ($candidates as $c) {
    try {
        $dsn = "mysql:host={$host};port={$port};dbname={$c['name']};charset=utf8mb4";
        $pdo = new PDO($dsn, $c['user'], $pass, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        $tables = (int) $pdo->query("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=" . $pdo->quote($c['name']))->fetchColumn();
        $products = 0;
        try {
            $products = (int) $pdo->query('SELECT COUNT(*) FROM products')->fetchColumn();
        } catch (Throwable $e) {
            // schema pas encore importé
        }
        $working = $c + ['tables' => $tables, 'products' => $products, 'pdo' => $pdo];
        break;
    } catch (Throwable $e) {
        $errors[] = $c['user'] . '@' . $c['name'] . ' → ' . $e->getMessage();
    }
}

echo '<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fix Yombal</title>';
echo '<style>body{font-family:system-ui,sans-serif;max-width:640px;margin:2rem auto;padding:0 1rem;line-height:1.45}code,pre{background:#f4f4f5;padding:.2rem .4rem;border-radius:4px}pre{padding:1rem;overflow:auto}.ok{color:#067647}.bad{color:#b42318}</style></head><body>';
echo '<h1>Yombal Market — réparation Hostinger</h1>';

if (!$working) {
    echo '<p class="bad"><strong>Aucune connexion MySQL n’a fonctionné.</strong></p><ul>';
    foreach ($errors as $err) {
        echo '<li><code>' . htmlspecialchars($err) . '</code></li>';
    }
    echo '</ul><p>Vérifiez dans hPanel → Bases de données MySQL le <strong>nom exact</strong> de la base, de l’utilisateur et le mot de passe. Puis rouvrez cette page.</p>';
    echo '<p>Dossier app : <code>' . htmlspecialchars($phpRoot) . '</code></p></body></html>';
    exit;
}

$env = <<<ENV
APP_NAME=Yombal Market
APP_URL=https://yombalmarket.com
APP_SECRET={$secret}
APP_DEBUG=0

DB_HOST=localhost
DB_PORT=3306
DB_NAME={$working['name']}
DB_USER={$working['user']}
DB_PASS={$pass}

ADMIN_EMAILS=compta@universdiasporas.com
CONTACT_EMAIL=compta@universdiasporas.com
PAYMENT_SIMULATION=0
ASSISTANT_ENABLED=1
INTERNATIONAL_SHIPPING_CENTS=1490
ENV;

if (file_put_contents($envPath, $env) === false) {
    echo '<p class="bad">Impossible d’écrire <code>' . htmlspecialchars($envPath) . '</code> (droits fichiers).</p></body></html>';
    exit;
}

echo '<p class="ok"><strong>.env créé</strong> → <code>' . htmlspecialchars($envPath) . '</code></p>';
echo '<p>Base : <code>' . htmlspecialchars($working['name']) . '</code><br>';
echo 'User : <code>' . htmlspecialchars($working['user']) . '</code><br>';
echo 'Tables : ' . (int) $working['tables'] . '<br>';
echo 'Produits : ' . (int) $working['products'] . '</p>';

if ((int) $working['tables'] < 5) {
    echo '<p class="bad"><strong>Schéma manquant.</strong> Dans phpMyAdmin, sélectionnez la base <code>'
        . htmlspecialchars($working['name']) . '</code> puis Importer :</p>';
    echo '<ol><li><code>php/sql/schema.sql</code></li><li><code>php/sql/products_seed.sql</code></li></ol>';
} elseif ((int) $working['products'] < 1) {
    echo '<p class="bad">Tables OK mais <strong>0 produit</strong>. Importez <code>php/sql/products_seed.sql</code>.</p>';
} else {
    echo '<p class="ok"><strong>Base OK.</strong> Ouvrez <a href="/">https://yombalmarket.com/</a></p>';
}

echo '<p class="bad"><strong>Supprimez immédiatement</strong> le fichier <code>fix.php</code> du serveur.</p>';
echo '</body></html>';
