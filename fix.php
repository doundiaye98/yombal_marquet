<?php
/**
 * Installation one-shot Hostinger — À SUPPRIMER après succès.
 * Ouvrir : https://yombalmarket.com/fix.php
 */
declare(strict_types=1);

header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex');
ini_set('display_errors', '1');
error_reporting(E_ALL);

$phpRoot = __DIR__ . '/php';
if (!is_dir($phpRoot . '/app')) {
    $phpRoot = __DIR__;
}
if (!is_dir($phpRoot . '/app')) {
    http_response_code(500);
    echo '<h1>Dossier php/app introuvable</h1><p>Attendu : <code>public_html/php/app/</code></p>';
    exit;
}

$envPath = $phpRoot . '/.env';
$defaultPass = 'UdBase2026!Paris';

// Base = u528552725_ymk | User Hostinger = u528552725_u528552725_ym (préfixe doublé à la création)
$dbName = trim((string) ($_POST['db_name'] ?? 'u528552725_ymk'));
$dbUser = trim((string) ($_POST['db_user'] ?? 'u528552725_u528552725_ym'));
$dbPass = (string) ($_POST['db_pass'] ?? $defaultPass);
$doSave = ($_SERVER['REQUEST_METHOD'] === 'POST');

echo '<!DOCTYPE html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fix Yombal MySQL</title>';
echo '<style>
body{font-family:system-ui,sans-serif;max-width:640px;margin:2rem auto;padding:0 1rem;line-height:1.45}
label{display:block;margin:.8rem 0 .25rem;font-weight:600}
input{width:100%;padding:.6rem;font-size:1rem;box-sizing:border-box}
button{margin-top:1rem;padding:.7rem 1.2rem;font-size:1rem;background:#001858;color:#fff;border:0;border-radius:8px}
.ok{color:#067647}.bad{color:#b42318}
code,pre{background:#f4f4f5;padding:.15rem .35rem;border-radius:4px}
pre{padding:1rem;overflow:auto;white-space:pre-wrap}
.box{border:1px solid #ddd;padding:1rem;border-radius:8px;margin:1rem 0;background:#fafafa}
</style></head><body>';
echo '<h1>Réparer MySQL — Yombal Market</h1>';
echo '<p>L’erreur <code>Access denied … (using password: YES)</code> signifie : mauvais <strong>utilisateur</strong>, <strong>mot de passe</strong> ou <strong>base</strong>.</p>';
echo '<div class="box"><strong>Où trouver les bons identifiants</strong><ol>';
echo '<li>hPanel Hostinger → <strong>Bases de données MySQL</strong></li>';
echo '<li>Notez le nom exact de la base (ex. <code>u528552725_ymk</code>)</li>';
echo '<li>Notez le nom exact de l’utilisateur</li>';
echo '<li>Si le mot de passe est oublié : <strong>Changer le mot de passe</strong> de l’utilisateur, puis collez-le ici</li>';
echo '</ol></div>';

echo '<form method="post">';
echo '<label>Nom de la base (DB_NAME)</label><input name="db_name" value="' . htmlspecialchars($dbName) . '" required>';
echo '<label>Utilisateur (DB_USER)</label><input name="db_user" value="' . htmlspecialchars($dbUser) . '" required>';
echo '<label>Mot de passe (DB_PASS)</label><input name="db_pass" type="text" value="' . htmlspecialchars($dbPass) . '" required autocomplete="off">';
echo '<button type="submit">Tester et enregistrer .env</button>';
echo '</form>';

if ($doSave) {
    echo '<hr><h2>Résultat</h2>';
    try {
        $dsn = 'mysql:host=localhost;port=3306;dbname=' . $dbName . ';charset=utf8mb4';
        $pdo = new PDO($dsn, $dbUser, $dbPass, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        $tables = (int) $pdo->query(
            'SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = ' . $pdo->quote($dbName)
        )->fetchColumn();
        $products = 0;
        try {
            $products = (int) $pdo->query('SELECT COUNT(*) FROM products')->fetchColumn();
        } catch (Throwable $e) {
            // pas encore de schéma
        }

        $secret = bin2hex(random_bytes(24));
        $env = "APP_NAME=Yombal Market\n"
            . "APP_URL=https://yombalmarket.com\n"
            . "APP_SECRET={$secret}\n"
            . "APP_DEBUG=0\n\n"
            . "DB_HOST=localhost\n"
            . "DB_PORT=3306\n"
            . "DB_NAME={$dbName}\n"
            . "DB_USER={$dbUser}\n"
            . 'DB_PASS="' . str_replace(['\\', '"'], ['\\\\', '\\"'], $dbPass) . "\"\n\n"
            . "ADMIN_EMAILS=compta@universdiasporas.com\n"
            . "CONTACT_EMAIL=compta@universdiasporas.com\n"
            . "PAYMENT_SIMULATION=0\n"
            . "ASSISTANT_ENABLED=1\n"
            . "INTERNATIONAL_SHIPPING_CENTS=1490\n";

        if (file_put_contents($envPath, $env) === false) {
            throw new RuntimeException('Impossible d’écrire ' . $envPath);
        }

        echo '<p class="ok"><strong>Connexion OK</strong> — .env enregistré dans <code>' . htmlspecialchars($envPath) . '</code></p>';
        echo '<p>Tables : ' . $tables . ' · Produits : ' . $products . '</p>';

        if ($tables < 5) {
            echo '<p class="bad">Importez dans phpMyAdmin (base sélectionnée) : <code>schema.sql</code> puis <code>products_seed.sql</code>.</p>';
        } elseif ($products < 1) {
            echo '<p class="bad">Importez <code>products_seed.sql</code>.</p>';
        } else {
            echo '<p class="ok"><a href="/">Ouvrir le site</a></p>';
        }
        echo '<p class="bad"><strong>Supprimez fix.php</strong> tout de suite.</p>';
    } catch (Throwable $e) {
        echo '<p class="bad"><strong>Échec :</strong> ' . htmlspecialchars($e->getMessage()) . '</p>';
        echo '<p>Vérifiez les 3 champs ci-dessus dans hPanel, ou <strong>réinitialisez le mot de passe</strong> MySQL puis réessayez.</p>';
    }
}

echo '</body></html>';
