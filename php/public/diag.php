<?php
/**
 * Diagnostic Hostinger — à supprimer après usage.
 * Ouvrir : https://votredomaine.com/diag.php
 */
declare(strict_types=1);
header('Content-Type: text/plain; charset=utf-8');
header('X-Robots-Tag: noindex');

$checks = [];
$ok = static function (string $label, bool $pass, string $detail = '') use (&$checks): void {
    $checks[] = ($pass ? '[OK]  ' : '[FAIL] ') . $label . ($detail !== '' ? " — {$detail}" : '');
};

$ok('PHP >= 8.1', version_compare(PHP_VERSION, '8.1.0', '>='), PHP_VERSION);
$ok('extension pdo_mysql', extension_loaded('pdo_mysql'));
$ok('extension mbstring', extension_loaded('mbstring'));
$ok('extension openssl', extension_loaded('openssl'));

$phpRoot = dirname(__DIR__);
$ok('dossier app/', is_dir($phpRoot . '/app'), $phpRoot . '/app');
$ok('fichier bootstrap.php', is_file($phpRoot . '/app/bootstrap.php'));
$ok('fichier .env', is_file($phpRoot . '/.env'), $phpRoot . '/.env');
$ok('dossier static/', is_dir(__DIR__ . '/static') || is_dir(__DIR__ . '/static/css'));
$ok('static/css/style.css', is_file(__DIR__ . '/static/css/style.css'));

$required = [
    'helpers.php', 'Database.php', 'Auth.php', 'Cart.php', 'Router.php',
    'Mailer.php', 'Shipping.php', 'ImmobilierData.php', 'EcosystemData.php', 'Assistant.php',
];
foreach ($required as $f) {
    $ok("app/{$f}", is_file($phpRoot . '/app/' . $f));
}

$dbDetail = 'non testé (.env manquant)';
$dbOk = false;
if (is_file($phpRoot . '/.env')) {
    foreach (file($phpRoot . '/.env', FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if ($line === '' || str_starts_with($line, '#') || !str_contains($line, '=')) {
            continue;
        }
        [$k, $v] = explode('=', $line, 2);
        $_ENV[trim($k)] = trim($v, " \t\"'");
    }
    $host = $_ENV['DB_HOST'] ?? 'localhost';
    $port = $_ENV['DB_PORT'] ?? '3306';
    $name = $_ENV['DB_NAME'] ?? '';
    $user = $_ENV['DB_USER'] ?? '';
    $pass = $_ENV['DB_PASS'] ?? '';
    try {
        $pdo = new PDO(
            "mysql:host={$host};port={$port};dbname={$name};charset=utf8mb4",
            $user,
            $pass,
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        );
        $n = (int) $pdo->query('SELECT COUNT(*) FROM products')->fetchColumn();
        $dbOk = true;
        $dbDetail = "connecté, {$n} produits";
    } catch (Throwable $e) {
        $dbDetail = $e->getMessage();
    }
}
$ok('MySQL + table products', $dbOk, $dbDetail);

echo "Yombal Market — diagnostic\n";
echo str_repeat('=', 40) . "\n";
echo implode("\n", $checks) . "\n";
echo str_repeat('=', 40) . "\n";
echo 'Document root: ' . __DIR__ . "\n";
echo 'Supprimez ce fichier (diag.php) après correction.' . "\n";
