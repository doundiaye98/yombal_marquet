<?php
declare(strict_types=1);

final class AdminController
{
    public static function login(): void
    {
        if (Auth::check() && Auth::isAdmin()) {
            redirect('/admin/');
        }
        if (is_post()) {
            verify_csrf();
            $email = strtolower(trim($_POST['email'] ?? ''));
            $password = $_POST['password'] ?? '';
            $user = Database::fetch('SELECT * FROM users WHERE email = ? AND is_active = 1', [$email]);
            if (!$user || !Password::verify($password, (string) $user['password_hash']) || !Auth::isAdmin($user)) {
                flash('Identifiants admin invalides.', 'danger');
            } else {
                Auth::login($user);
                redirect('/admin/');
            }
        }
        view('admin/login', ['ep' => 'admin.login', 'page_title' => 'Admin — Connexion', 'main_class' => 'admin-main']);
    }

    public static function logout(): void
    {
        Auth::logout();
        redirect('/admin/connexion');
    }

    public static function dashboard(): void
    {
        Auth::requireAdmin();
        $orders = (int) (Database::fetch('SELECT COUNT(*) AS c FROM orders')['c'] ?? 0);
        $products = (int) (Database::fetch('SELECT COUNT(*) AS c FROM products WHERE is_active = 1')['c'] ?? 0);
        $unread = (int) (Database::fetch('SELECT COUNT(*) AS c FROM contact_messages WHERE is_read = 0')['c'] ?? 0);
        $recent = Database::fetchAll('SELECT * FROM orders ORDER BY created_at DESC LIMIT 10');
        view('admin/dashboard', [
            'ep' => 'admin.dashboard',
            'page_title' => 'Admin',
            'stats' => compact('orders', 'products', 'unread'),
            'recent' => $recent,
            'main_class' => 'admin-main',
        ]);
    }

    public static function products(): void
    {
        Auth::requireAdmin();
        $products = Database::fetchAll('SELECT * FROM products ORDER BY category, name');
        view('admin/products', [
            'ep' => 'admin.products',
            'page_title' => 'Produits',
            'products' => $products,
            'main_class' => 'admin-main',
        ]);
    }

    public static function productForm(?string $id = null): void
    {
        Auth::requireAdmin();
        $product = null;
        if ($id) {
            $product = Database::fetch('SELECT * FROM products WHERE id = ?', [(int) $id]);
            if (!$product) {
                flash('Produit introuvable.', 'danger');
                redirect('/admin/produits');
            }
        }
        if (is_post()) {
            verify_csrf();
            $data = [
                'sku' => trim($_POST['sku'] ?? '') ?: null,
                'slug' => trim($_POST['slug'] ?? ''),
                'name' => trim($_POST['name'] ?? ''),
                'summary' => trim($_POST['summary'] ?? '') ?: null,
                'description' => trim($_POST['description'] ?? ''),
                'price_cents' => (int) round(((float) str_replace(',', '.', $_POST['price_euros'] ?? '0')) * 100),
                'category' => trim($_POST['category'] ?? 'miels'),
                'origin' => trim($_POST['origin'] ?? '') ?: null,
                'weight_info' => trim($_POST['weight_info'] ?? '') ?: null,
                'stock_qty' => ($_POST['stock_qty'] ?? '') === '' ? null : (int) $_POST['stock_qty'],
                'image' => trim($_POST['image'] ?? '') ?: null,
                'icon' => trim($_POST['icon'] ?? '') ?: null,
                'is_active' => isset($_POST['is_active']) ? 1 : 0,
            ];
            if ($data['slug'] === '' || $data['name'] === '' || $data['description'] === '') {
                flash('Slug, nom et description obligatoires.', 'danger');
            } else {
                if ($product) {
                    Database::update('products', $data, 'id = :id', ['id' => (int) $product['id']]);
                    flash('Produit mis à jour.', 'success');
                    redirect('/admin/produit/' . $product['id']);
                } else {
                    $newId = Database::insert('products', $data);
                    flash('Produit créé.', 'success');
                    redirect('/admin/produit/' . $newId);
                }
            }
        }
        view('admin/product_form', [
            'ep' => 'admin.product_form',
            'page_title' => $product ? 'Modifier produit' : 'Nouveau produit',
            'product' => $product,
            'categories' => category_labels(),
            'main_class' => 'admin-main',
        ]);
    }

    public static function productDelete(string $id): void
    {
        Auth::requireAdmin();
        verify_csrf();
        Database::update('products', ['is_active' => 0], 'id = :id', ['id' => (int) $id]);
        flash('Produit désactivé.', 'success');
        redirect('/admin/produits');
    }

    public static function orders(): void
    {
        Auth::requireAdmin();
        $orders = Database::fetchAll('SELECT * FROM orders ORDER BY created_at DESC LIMIT 100');
        view('admin/orders', [
            'ep' => 'admin.orders',
            'page_title' => 'Commandes',
            'orders' => $orders,
            'main_class' => 'admin-main',
        ]);
    }

    public static function orderDetail(string $id): void
    {
        Auth::requireAdmin();
        $order = Database::fetch('SELECT * FROM orders WHERE id = ?', [(int) $id]);
        if (!$order) {
            flash('Commande introuvable.', 'danger');
            redirect('/admin/commandes');
        }
        if (is_post()) {
            verify_csrf();
            $new = trim($_POST['status'] ?? '');
            $allowed = ['pending', 'awaiting_wire', 'awaiting_paypal', 'cod_confirmed', 'paid_manual', 'paid_stripe', 'shipped', 'cancelled'];
            if (in_array($new, $allowed, true) && $new !== $order['status']) {
                $old = $order['status'];
                Database::update('orders', ['status' => $new], 'id = :id', ['id' => (int) $id]);
                Database::insert('order_status_events', [
                    'order_id' => (int) $id,
                    'from_status' => $old,
                    'to_status' => $new,
                    'note' => trim($_POST['note'] ?? '') ?: 'Mise à jour admin',
                    'actor_user_id' => Auth::user()['id'] ?? null,
                ]);
                flash('Statut mis à jour.', 'success');
                redirect('/admin/commande/' . $id);
            }
        }
        $items = Database::fetchAll('SELECT * FROM order_items WHERE order_id = ?', [(int) $id]);
        $events = Database::fetchAll(
            'SELECT * FROM order_status_events WHERE order_id = ? ORDER BY created_at ASC',
            [(int) $id]
        );
        view('admin/order_detail', [
            'ep' => 'admin.order_detail',
            'page_title' => $order['public_ref'],
            'order' => $order,
            'items' => $items,
            'events' => $events,
            'main_class' => 'admin-main',
        ]);
    }

    public static function messages(): void
    {
        Auth::requireAdmin();
        $messages = Database::fetchAll('SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 100');
        view('admin/messages', [
            'ep' => 'admin.messages',
            'page_title' => 'Messages',
            'messages' => $messages,
            'main_class' => 'admin-main',
        ]);
    }

    public static function messageRead(string $id): void
    {
        Auth::requireAdmin();
        verify_csrf();
        Database::update('contact_messages', ['is_read' => 1], 'id = :id', ['id' => (int) $id]);
        redirect('/admin/messages');
    }
}
