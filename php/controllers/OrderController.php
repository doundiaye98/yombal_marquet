<?php
declare(strict_types=1);

final class OrderController
{
    public static function suivi(): void
    {
        $recent = [];
        if (Auth::check()) {
            $recent = Database::fetchAll(
                'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC LIMIT 20',
                [(int) Auth::user()['id']]
            );
        } else {
            $ids = Cart::guestOrderIds();
            if ($ids) {
                $in = implode(',', array_fill(0, count($ids), '?'));
                $recent = Database::fetchAll(
                    "SELECT * FROM orders WHERE id IN ($in) ORDER BY created_at DESC",
                    $ids
                );
            }
        }

        if (is_post()) {
            verify_csrf();
            $ref = strtoupper(trim($_POST['public_ref'] ?? ''));
            $email = strtolower(trim($_POST['email'] ?? ''));
            $order = Database::fetch(
                'SELECT * FROM orders WHERE public_ref = ? AND (guest_email = ? OR user_id IN (SELECT id FROM users WHERE email = ?))',
                [$ref, $email, $email]
            );
            if (!$order) {
                flash('Aucune commande trouvée pour cette référence et cet e-mail.', 'danger');
            } else {
                Cart::rememberGuestOrder((int) $order['id']);
                redirect('/suivi-commande/' . $order['id']);
            }
        }

        view('orders/suivi', [
            'ep' => 'suivi_commande',
            'page_title' => 'Mes commandes — Yombal Marché',
            'recent_orders' => $recent,
            'tracking_email' => $_POST['email'] ?? (Auth::check() ? (Auth::user()['email'] ?? '') : ''),
            'tracking_ref' => $_POST['public_ref'] ?? ($_POST['order_ref'] ?? ''),
        ]);
    }

    public static function detail(string $orderId): void
    {
        $order = CheckoutController::loadAccessibleOrder((int) $orderId);
        $items = Database::fetchAll('SELECT * FROM order_items WHERE order_id = ?', [(int) $orderId]);
        $events = Database::fetchAll(
            'SELECT * FROM order_status_events WHERE order_id = ? ORDER BY created_at ASC',
            [(int) $orderId]
        );
        view('orders/detail', [
            'ep' => 'suivi_commande_detail',
            'page_title' => 'Commande ' . $order['public_ref'],
            'order' => $order,
            'items' => $items,
            'events' => $events,
            'confirmed' => isset($_GET['confirmed']),
        ]);
    }

    public static function annuler(string $orderId): void
    {
        verify_csrf();
        $order = CheckoutController::loadAccessibleOrder((int) $orderId);
        $cancellable = ['pending', 'awaiting_wire', 'awaiting_paypal', 'cod_confirmed'];
        if (!in_array($order['status'], $cancellable, true)) {
            flash('Cette commande ne peut plus être annulée.', 'warning');
            redirect('/suivi-commande/' . $orderId);
        }
        $pdo = Database::pdo();
        $pdo->beginTransaction();
        try {
            $items = Database::fetchAll('SELECT * FROM order_items WHERE order_id = ?', [(int) $orderId]);
            foreach ($items as $it) {
                Database::query(
                    'UPDATE products SET stock_qty = stock_qty + ? WHERE id = ? AND stock_qty IS NOT NULL',
                    [(int) $it['quantity'], (int) $it['product_id']]
                );
            }
            $old = $order['status'];
            Database::update('orders', ['status' => 'cancelled'], 'id = :id', ['id' => (int) $orderId]);
            Database::insert('order_status_events', [
                'order_id' => (int) $orderId,
                'from_status' => $old,
                'to_status' => 'cancelled',
                'note' => 'Annulation client',
                'actor_user_id' => Auth::user()['id'] ?? null,
            ]);
            $pdo->commit();
            flash('Commande annulée.', 'success');
        } catch (Throwable $e) {
            $pdo->rollBack();
            flash('Impossible d\'annuler la commande.', 'danger');
        }
        redirect('/suivi-commande/' . $orderId);
    }

    public static function recommander(string $orderId): void
    {
        verify_csrf();
        $order = CheckoutController::loadAccessibleOrder((int) $orderId);
        $items = Database::fetchAll('SELECT * FROM order_items WHERE order_id = ?', [(int) $orderId]);
        foreach ($items as $it) {
            Cart::add((int) $it['product_id'], (int) $it['quantity']);
        }
        flash('Articles ajoutés au panier.', 'success');
        redirect('/panier');
    }
}
