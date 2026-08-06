<?php
declare(strict_types=1);

final class Cart
{
    private static function bag(): array
    {
        if (!isset($_SESSION['cart']) || !is_array($_SESSION['cart'])) {
            $_SESSION['cart'] = [];
        }
        return $_SESSION['cart'];
    }

    private static function save(array $bag): void
    {
        $_SESSION['cart'] = $bag;
    }

    public static function count(): int
    {
        $n = 0;
        foreach (self::bag() as $qty) {
            $n += (int) $qty;
        }
        return $n;
    }

    public static function add(int $productId, int $qty = 1): array
    {
        $qty = max(1, $qty);
        $product = Database::fetch(
            'SELECT * FROM products WHERE id = ? AND is_active = 1',
            [$productId]
        );
        if (!$product) {
            return [false, 'Produit introuvable.'];
        }
        if ($product['stock_qty'] !== null && (int) $product['stock_qty'] < $qty) {
            return [false, 'Stock insuffisant.'];
        }
        $bag = self::bag();
        $key = (string) $productId;
        $bag[$key] = ($bag[$key] ?? 0) + $qty;
        if ($product['stock_qty'] !== null && $bag[$key] > (int) $product['stock_qty']) {
            return [false, 'Stock insuffisant.'];
        }
        self::save($bag);
        return [true, null];
    }

    public static function setQty(int $productId, ?int $qty): array
    {
        $bag = self::bag();
        $key = (string) $productId;
        if ($qty === null || $qty <= 0) {
            unset($bag[$key]);
            self::save($bag);
            return [true, null];
        }
        $product = Database::fetch(
            'SELECT * FROM products WHERE id = ? AND is_active = 1',
            [$productId]
        );
        if (!$product) {
            return [false, 'Produit introuvable.'];
        }
        if ($product['stock_qty'] !== null && (int) $product['stock_qty'] < $qty) {
            return [false, 'Stock insuffisant.'];
        }
        $bag[$key] = $qty;
        self::save($bag);
        return [true, null];
    }

    public static function clear(): void
    {
        self::save([]);
    }

    /** @return array{0: list<array>, 1: int} */
    public static function items(): array
    {
        $bag = self::bag();
        if (!$bag) {
            return [[], 0];
        }
        $ids = array_map('intval', array_keys($bag));
        $placeholders = implode(',', array_fill(0, count($ids), '?'));
        $products = Database::fetchAll(
            "SELECT * FROM products WHERE id IN ($placeholders) AND is_active = 1",
            $ids
        );
        $byId = [];
        foreach ($products as $p) {
            $byId[(int) $p['id']] = $p;
        }
        $rows = [];
        $total = 0;
        foreach ($bag as $pid => $qty) {
            $pid = (int) $pid;
            $qty = (int) $qty;
            if (!isset($byId[$pid]) || $qty < 1) {
                continue;
            }
            $p = $byId[$pid];
            $line = (int) $p['price_cents'] * $qty;
            $total += $line;
            $rows[] = [
                'product' => $p,
                'quantity' => $qty,
                'line_total_cents' => $line,
            ];
        }
        return [$rows, $total];
    }

    public static function rememberGuestOrder(int $orderId): void
    {
        $ids = $_SESSION['guest_orders'] ?? [];
        if (!is_array($ids)) {
            $ids = [];
        }
        $ids[] = $orderId;
        $_SESSION['guest_orders'] = array_values(array_unique(array_map('intval', $ids)));
    }

    public static function guestOrderIds(): array
    {
        $ids = $_SESSION['guest_orders'] ?? [];
        return is_array($ids) ? array_map('intval', $ids) : [];
    }
}
