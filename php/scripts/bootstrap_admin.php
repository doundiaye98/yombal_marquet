<?php
declare(strict_types=1);
/**
 * Crée / met à jour les comptes ADMIN_EMAILS avec BOOTSTRAP_ADMIN_PASSWORD.
 * Usage (CLI) : php scripts/bootstrap_admin.php
 * Ou navigateur une seule fois : /scripts/bootstrap_admin.php (à supprimer après)
 */
require dirname(__DIR__) . '/app/bootstrap.php';

$password = env('BOOTSTRAP_ADMIN_PASSWORD');
if (!$password || strlen($password) < 8) {
    fwrite(STDERR, "Définissez BOOTSTRAP_ADMIN_PASSWORD (≥ 8 car.) dans .env\n");
    exit(1);
}

$emails = array_filter(array_map('trim', explode(',', env('ADMIN_EMAILS', '') ?? '')));
if (!$emails) {
    fwrite(STDERR, "ADMIN_EMAILS vide\n");
    exit(1);
}

foreach ($emails as $email) {
    $email = strtolower($email);
    $existing = Database::fetch('SELECT * FROM users WHERE email = ?', [$email]);
    $hash = Password::hash($password);
    if ($existing) {
        Database::update('users', ['password_hash' => $hash, 'is_active' => 1], 'id = :id', ['id' => $existing['id']]);
        echo "Mis à jour: {$email}\n";
    } else {
        Database::insert('users', [
            'email' => $email,
            'password_hash' => $hash,
            'name' => 'Admin',
            'is_active' => 1,
        ]);
        echo "Créé: {$email}\n";
    }
}
echo "OK. Supprimez BOOTSTRAP_ADMIN_PASSWORD du .env après connexion.\n";
