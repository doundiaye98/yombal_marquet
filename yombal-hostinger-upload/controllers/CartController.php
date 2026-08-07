<?php
declare(strict_types=1);

final class CartController
{
    public static function show(): void
    {
        [$items, $total] = Cart::items();
        view('cart', ['ep' => 'panier', 'page_title' => 'Panier — Yombal Marché', 'items' => $items, 'total_cents' => $total, 'cart_item_count' => Cart::count()]);
    }

    public static function add(): void
    {
        verify_csrf();
        $pid = (int) ($_POST['product_id'] ?? 0);
        $qty = (int) ($_POST['quantity'] ?? 1);
        if (!$pid) { flash('Produit introuvable.', 'danger'); redirect('/boutique'); }
        [$ok, $err] = Cart::add($pid, $qty);
        $product = Database::fetch('SELECT slug FROM products WHERE id = ?', [$pid]);
        if (!$ok) { flash($err ?: 'Produit introuvable.', 'danger'); redirect('/boutique'); }
        flash('Produit ajouté au panier.', 'success');
        redirect($product ? '/produit/' . $product['slug'] : '/panier');
    }

    public static function update(): void
    {
        verify_csrf();
        $pid = (int) ($_POST['product_id'] ?? 0);
        $qty = isset($_POST['quantity']) ? (int) $_POST['quantity'] : 0;
        [$ok, $err] = Cart::setQty($pid, $qty);
        if (!$ok && $err) flash($err, 'warning');
        redirect('/panier');
    }
}
