<?php
declare(strict_types=1);

final class Shipping
{
    public static function compute(string $country, string $postalCode, int $subtotalCents): int
    {
        $country = strtoupper($country);
        if ($country !== 'FR') {
            return (int) env('INTERNATIONAL_SHIPPING_CENTS', '1490');
        }
        $zones = Database::fetchAll(
            'SELECT * FROM delivery_zones WHERE is_active = 1 ORDER BY sort_order ASC, id ASC'
        );
        $prefix = substr(preg_replace('/\s+/', '', $postalCode) ?? '', 0, 2);
        $chosen = null;
        foreach ($zones as $z) {
            $zp = trim((string) ($z['postal_prefix'] ?? ''));
            if ($zp === '' || $zp === null) {
                $chosen = $z;
                continue;
            }
            if ($prefix !== '' && str_starts_with($prefix, $zp)) {
                $chosen = $z;
                break;
            }
        }
        if (!$chosen) {
            return 590;
        }
        $price = (int) $chosen['price_cents'];
        $freeOver = $chosen['free_over_cents'];
        if ($freeOver !== null && $subtotalCents >= (int) $freeOver) {
            return 0;
        }
        return $price;
    }
}
