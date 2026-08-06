<?php
declare(strict_types=1);

final class Auth
{
    public static function user(): ?array
    {
        $id = $_SESSION['user_id'] ?? null;
        if (!$id) {
            return null;
        }
        static $cache = null;
        if ($cache !== null && (int) $cache['id'] === (int) $id) {
            return $cache;
        }
        $cache = Database::fetch('SELECT * FROM users WHERE id = ? AND is_active = 1', [(int) $id]);
        if (!$cache) {
            unset($_SESSION['user_id']);
            return null;
        }
        return $cache;
    }

    public static function check(): bool
    {
        return self::user() !== null;
    }

    public static function login(array $user): void
    {
        session_regenerate_id(true);
        $_SESSION['user_id'] = (int) $user['id'];
    }

    public static function logout(): void
    {
        unset($_SESSION['user_id']);
        session_regenerate_id(true);
    }

    public static function isAdmin(?array $user = null): bool
    {
        $user = $user ?? self::user();
        if (!$user) {
            return false;
        }
        $emails = array_filter(array_map('trim', explode(',', env('ADMIN_EMAILS', env('CONTACT_EMAIL', '') ?? '') ?? '')));
        $emails = array_map('strtolower', $emails);
        return in_array(strtolower((string) $user['email']), $emails, true);
    }

    public static function requireLogin(): array
    {
        $u = self::user();
        if (!$u) {
            flash('Connectez-vous pour continuer.', 'warning');
            redirect('/auth/connexion');
        }
        return $u;
    }

    public static function requireAdmin(): array
    {
        $u = self::requireLogin();
        if (!self::isAdmin($u)) {
            http_response_code(403);
            exit('Accès admin refusé.');
        }
        return $u;
    }
}
