<?php
declare(strict_types=1);

final class CheckoutController
{
    public static function checkout(): void
    {
        [$items, $subtotal] = Cart::items();
        if (!$items) { flash('Votre panier est vide.', 'warning'); redirect('/boutique'); }
        $user = Auth::user();
        $form = ['guest_email'=>$user['email'] ?? '','guest_name'=>$user['name'] ?? '','guest_phone'=>$user['phone'] ?? '','customer_phone'=>$user['phone'] ?? '','delivery_line1'=>'','delivery_line2'=>'','delivery_city'=>'','delivery_postal_code'=>'','delivery_country'=>'FR','customer_notes'=>'','promo_code'=>'','gift_message'=>'','is_gift'=>'0'];
        $shipping = Shipping::compute('FR', '', $subtotal);
        $discount = 0; $promoCode = ''; $total = max(0, $subtotal + $shipping);
        if (is_post()) {
            verify_csrf();
            foreach (array_keys($form) as $k) if (isset($_POST[$k])) $form[$k] = trim((string) $_POST[$k]);
            $promoCode = strtoupper(trim($form['promo_code']));
            $shipping = Shipping::compute(strtoupper($form['delivery_country'] ?: 'FR'), $form['delivery_postal_code'], $subtotal);
            $total = max(0, $subtotal + $shipping - $discount);
            if (!$user && !str_contains($form['guest_email'], '@')) flash('Indiquez un e-mail valide.', 'danger');
            elseif (strlen($form['delivery_line1']) < 5) flash('Indiquez une adresse de livraison complète.', 'danger');
            elseif (strlen($form['delivery_city']) < 2) flash('Indiquez la ville.', 'danger');
            elseif (strlen($form['delivery_postal_code']) < 2) flash('Indiquez un code postal valide.', 'danger');
            else {
                $pdo = Database::pdo(); $pdo->beginTransaction();
                try {
                    $ref = 'YM-' . date('Ymd') . '-' . strtoupper(bin2hex(random_bytes(3)));
                    $orderId = Database::insert('orders', ['public_ref'=>$ref,'user_id'=>$user ? (int) $user['id'] : null,'guest_email'=>$user ? $user['email'] : $form['guest_email'],'guest_name'=>$user ? ($user['name'] ?: $form['guest_name']) : $form['guest_name'],'guest_phone'=>$form['customer_phone'] ?: null,'delivery_line1'=>$form['delivery_line1'],'delivery_line2'=>$form['delivery_line2'] ?: null,'delivery_city'=>$form['delivery_city'],'delivery_postal_code'=>$form['delivery_postal_code'],'delivery_country'=>strtoupper($form['delivery_country'] ?: 'FR'),'customer_notes'=>$form['customer_notes'] ?: null,'gift_message'=>$form['gift_message'] ?: null,'is_gift'=>$form['is_gift'] === '1' ? 1 : 0,'promo_code'=>$promoCode ?: null,'discount_cents'=>$discount,'currency'=>'EUR','subtotal_cents'=>$subtotal,'shipping_cents'=>$shipping,'total_cents'=>$total,'status'=>'pending']);
                    foreach ($items as $row) {
                        $p = $row['product'];
                        Database::insert('order_items', ['order_id'=>$orderId,'product_id'=>(int) $p['id'],'product_name'=>$p['name'],'quantity'=>(int) $row['quantity'],'unit_price_cents'=>(int) $p['price_cents'],'line_total_cents'=>(int) $row['line_total_cents']]);
                    }
                    Database::insert('order_status_events', ['order_id'=>$orderId,'from_status'=>null,'to_status'=>'pending','note'=>'Commande créée','actor_user_id'=>$user ? (int) $user['id'] : null]);
                    $pdo->commit();
                    Cart::clear();
                    if (!$user) Cart::rememberGuestOrder($orderId);
                    flash('Commande créée. Choisissez votre mode de paiement.', 'success');
                    redirect('/paiement/' . $orderId);
                } catch (Throwable $e) { $pdo->rollBack(); flash('Erreur lors de la création de la commande.', 'danger'); }
            }
        }
        view('checkout', ['ep'=>'checkout','page_title'=>'Commande — Yombal Marché','items'=>$items,'subtotal_cents'=>$subtotal,'shipping_cents'=>$shipping,'discount_cents'=>$discount,'total_cents'=>$total,'guest_form'=>$form,'promo_code'=>$promoCode,'delivery_countries'=>['FR'=>'France','SN'=>'Sénégal','BE'=>'Belgique','CH'=>'Suisse','DE'=>'Allemagne','ES'=>'Espagne','IT'=>'Italie']]);
    }

    public static function paiement(string $orderId): void
    {
        $order = self::loadAccessibleOrder((int) $orderId);
        $items = Database::fetchAll('SELECT * FROM order_items WHERE order_id = ?', [(int) $orderId]);
        view('paiement', ['ep'=>'paiement','page_title'=>'Paiement — ' . $order['public_ref'],'order'=>$order,'items'=>$items,'stripe_ok'=>(bool) env('STRIPE_SECRET_KEY') && (bool) env('STRIPE_PUBLISHABLE_KEY'),'stripe_publishable'=>env('STRIPE_PUBLISHABLE_KEY', ''),'bank'=>['name'=>env('BANK_NAME', ''),'holder'=>env('BANK_HOLDER', ''),'iban'=>env('BANK_IBAN', ''),'bic'=>env('BANK_BIC', '')],'paypal_email'=>env('PAYPAL_EMAIL', ''),'paypal_me'=>env('PAYPAL_ME_URL', ''),'payment_simulation'=>env('PAYMENT_SIMULATION', '0') === '1']);
    }

    public static function paiementManuel(string $orderId): void
    {
        verify_csrf(); $order = self::loadAccessibleOrder((int) $orderId); $method = $_POST['payment_method'] ?? ''; $map = ['wire'=>'awaiting_wire','paypal'=>'awaiting_paypal','cash_delivery'=>'cod_confirmed']; if (!isset($map[$method])) { flash('Mode de paiement invalide.', 'danger'); redirect('/paiement/' . $orderId); }
        Database::update('orders', ['status'=>$map[$method],'payment_method'=>$method], 'id = :id', ['id'=>(int) $orderId]);
        Database::insert('order_status_events', ['order_id'=>(int) $orderId,'from_status'=>$order['status'],'to_status'=>$map[$method],'note'=>'Choix paiement client','actor_user_id'=>Auth::user()['id'] ?? null]);
        flash('Mode de paiement enregistré.', 'success'); redirect('/suivi-commande/' . $orderId . '?confirmed=1');
    }

    public static function paiementDemo(string $orderId): void
    {
        verify_csrf(); if (env('PAYMENT_SIMULATION', '0') !== '1') { http_response_code(403); exit('Simulation désactivée.'); } $order = self::loadAccessibleOrder((int) $orderId);
        Database::update('orders', ['status'=>'paid_demo','payment_method'=>'demo'], 'id = :id', ['id'=>(int) $orderId]);
        Database::insert('order_status_events', ['order_id'=>(int) $orderId,'from_status'=>$order['status'],'to_status'=>'paid_demo','note'=>'Paiement simulé','actor_user_id'=>Auth::user()['id'] ?? null]);
        flash('Paiement simulé enregistré.', 'success'); redirect('/suivi-commande/' . $orderId . '?confirmed=1');
    }

    public static function loadAccessibleOrder(int $orderId): array
    {
        $order = Database::fetch('SELECT * FROM orders WHERE id = ?', [$orderId]); if (!$order) { http_response_code(404); exit('Commande introuvable.'); }
        $user = Auth::user(); $ok = false;
        if ($user && (int) ($order['user_id'] ?? 0) === (int) $user['id']) $ok = true;
        if (in_array($orderId, Cart::guestOrderIds(), true)) $ok = true;
        if (Auth::isAdmin()) $ok = true;
        if (!$ok) { http_response_code(403); exit('Accès à cette commande refusé.'); }
        return $order;
    }
}
