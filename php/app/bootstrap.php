<?php
declare(strict_types=1);

/**
 * Bootstrap application PHP Yombal Market
 */

define('PHP_ROOT', dirname(__DIR__));

require PHP_ROOT . '/app/helpers.php';
require PHP_ROOT . '/app/Database.php';
require PHP_ROOT . '/app/Password.php';
require PHP_ROOT . '/app/Auth.php';
require PHP_ROOT . '/app/Cart.php';
require PHP_ROOT . '/app/Router.php';
require PHP_ROOT . '/app/Mailer.php';
require PHP_ROOT . '/app/Shipping.php';
require PHP_ROOT . '/app/ImmobilierData.php';
require PHP_ROOT . '/app/EcosystemData.php';
require PHP_ROOT . '/app/Assistant.php';

// Charge .env (plusieurs emplacements possibles selon le déploiement Hostinger)
$envCandidates = [
    PHP_ROOT . '/.env',
    PHP_ROOT . '/.env.hostinger',
    dirname(PHP_ROOT) . '/.env',
];
$envFile = null;
foreach ($envCandidates as $candidate) {
    if (is_file($candidate)) {
        $envFile = $candidate;
        break;
    }
}
if ($envFile !== null) {
    foreach (file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $line = trim($line);
        if ($line === '' || str_starts_with($line, '#') || !str_contains($line, '=')) {
            continue;
        }
        [$k, $v] = explode('=', $line, 2);
        $k = trim($k);
        $v = trim($v, " \t\"'");
        $_ENV[$k] = $v;
        putenv("{$k}={$v}");
    }
}

// URL de base auto (si APP_URL vide)
$scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
$host = $_SERVER['HTTP_HOST'] ?? 'localhost';
$basePath = rtrim(str_replace('\\', '/', dirname($_SERVER['SCRIPT_NAME'] ?? '')), '/');
$autoUrl = $scheme . '://' . $host . ($basePath === '/' ? '' : $basePath);

$GLOBALS['app_config'] = [
    'app_url' => rtrim(env('APP_URL', $autoUrl) ?? $autoUrl, '/'),
    'app_name' => env('APP_NAME', 'Yombal Market'),
    'debug' => env('APP_DEBUG', '0') === '1',
];

ini_set('session.cookie_httponly', '1');
ini_set('session.use_strict_mode', '1');
if (session_status() !== PHP_SESSION_ACTIVE) {
    session_name('yombal_sess');
    session_start();
}

date_default_timezone_set('Europe/Paris');

if (config('debug')) {
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
} else {
    error_reporting(E_ALL & ~E_NOTICE & ~E_DEPRECATED);
    ini_set('display_errors', '0');
}

require PHP_ROOT . '/controllers/ShopController.php';
require PHP_ROOT . '/controllers/AuthController.php';
require PHP_ROOT . '/controllers/CartController.php';
require PHP_ROOT . '/controllers/CheckoutController.php';
require PHP_ROOT . '/controllers/OrderController.php';
require PHP_ROOT . '/controllers/PageController.php';
require PHP_ROOT . '/controllers/AdminController.php';
