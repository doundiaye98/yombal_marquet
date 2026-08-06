<?php
declare(strict_types=1);

final class AuthController
{
    public static function register(): void
    {
        if (Auth::check()) {
            redirect('/compte');
        }
        if (is_post()) {
            verify_csrf();
            $email = strtolower(trim($_POST['email'] ?? ''));
            $password = $_POST['password'] ?? '';
            $name = trim($_POST['name'] ?? '');
            if (!$email || !str_contains($email, '@')) {
                flash('Adresse e-mail invalide.', 'danger');
            } elseif (strlen($password) < 6) {
                flash('Mot de passe : au moins 6 caractères.', 'danger');
            } elseif (Database::fetch('SELECT id FROM users WHERE email = ?', [$email])) {
                flash('Un compte existe déjà avec cet e-mail.', 'danger');
            } else {
                $id = Database::insert('users', [
                    'email' => $email,
                    'password_hash' => Password::hash($password),
                    'name' => $name !== '' ? $name : null,
                    'is_active' => 1,
                ]);
                $user = Database::fetch('SELECT * FROM users WHERE id = ?', [$id]);
                Auth::login($user);
                flash('Compte créé. Bienvenue dans votre espace client.', 'success');
                redirect('/compte');
            }
        }
        view('auth/register', ['ep' => 'register', 'page_title' => 'Inscription']);
    }

    public static function login(): void
    {
        if (Auth::check()) {
            redirect('/compte');
        }
        if (is_post()) {
            verify_csrf();
            $email = strtolower(trim($_POST['email'] ?? ''));
            $password = $_POST['password'] ?? '';
            $user = Database::fetch('SELECT * FROM users WHERE email = ? AND is_active = 1', [$email]);
            if (!$user || !Password::verify($password, (string) $user['password_hash'])) {
                flash('E-mail ou mot de passe incorrect.', 'danger');
            } else {
                // Re-hash Werkzeug → bcrypt PHP si besoin
                if (str_starts_with((string) $user['password_hash'], 'pbkdf2:')) {
                    Database::update('users', ['password_hash' => Password::hash($password)], 'id = :id', ['id' => $user['id']]);
                }
                Auth::login($user);
                flash('Connexion réussie.', 'success');
                $next = $_GET['next'] ?? '/compte';
                if (!str_starts_with($next, '/') || str_starts_with($next, '//')) {
                    $next = '/compte';
                }
                redirect($next);
            }
        }
        view('auth/login', ['ep' => 'login', 'page_title' => 'Connexion — Yombal Market', 'next' => $_GET['next'] ?? '', 'old_email' => $_POST['email'] ?? '']);
    }

    public static function logout(): void
    {
        Auth::logout();
        flash('Vous êtes déconnecté.', 'success');
        redirect('/');
    }

    public static function compte(): void
    {
        $user = Auth::requireLogin();
        $orders = Database::fetchAll(
            'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 30',
            [(int) $user['id']]
        );
        view('auth/compte', [
            'ep' => 'compte',
            'page_title' => 'Mon compte',
            'orders' => $orders,
            'user' => $user,
        ]);
    }
}
