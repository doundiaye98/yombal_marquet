<?php
declare(strict_types=1);

final class ShopController
{
    public static function index(): void
    {
        $featured = Database::fetchAll('SELECT * FROM products WHERE is_active = 1 ORDER BY id ASC LIMIT 6');
        $phareSlugs = ['arraw-mil-labelafrik','thiakry-400g','sankhal-labelafrik','thiere-lalo-labelafrik','fonio-500g','bouye-baobab-250g'];
        $placeholders = implode(',', array_fill(0, count($phareSlugs), '?'));
        $pharesRaw = Database::fetchAll("SELECT * FROM products WHERE is_active = 1 AND slug IN ($placeholders)", $phareSlugs);
        $bySlug = [];
        foreach ($pharesRaw as $p) $bySlug[$p['slug']] = $p;
        $catalogue_phares = [];
        foreach ($phareSlugs as $s) if (isset($bySlug[$s])) $catalogue_phares[] = $bySlug[$s];
        $recipes = Database::fetchAll('SELECT * FROM recipes WHERE is_active = 1 ORDER BY id ASC LIMIT 3');
        foreach ($recipes as &$r) { $r['emoji'] = '🍲'; $r['kind_label'] = $r['type'] ?: 'Recette'; $r['total_cents'] = 0; }
        $product_count = (int) (Database::fetch('SELECT COUNT(*) AS c FROM products WHERE is_active = 1')['c'] ?? 0);
        view('home', [
            'ep' => 'index',
            'page_title' => 'Yombal Market — Votre marché en poche',
            'featured_products' => $featured,
            'featured_recipes' => $recipes,
            'catalogue_phares' => $catalogue_phares,
            'product_count' => $product_count,
            'extra_css' => '<link rel="stylesheet" href="' . e(asset('css/home-marketplace.css')) . '">',
            'extra_scripts' => '<script src="' . e(asset('js/home-experience.js')) . '" defer></script>',
        ]);
    }

    public static function boutique(): void
    {
        $filter_cat = $_GET['categorie'] ?? null;
        $filter_type = $_GET['type'] ?? null;
        $shopTypeAlimentaire = 'alimentaire';
        $shopTypeNonAlimentaire = 'non-alimentaire';
        $shopRayons = ['cereales','legumineuses','huiles','snacks','desserts','boissons','condiments','fruits','legumes','conserves','poisson','viandes','cosmetique','electronique','electromenager','mode','chaussures','bagagerie'];
        $shopUniverseLabels = [
            $shopTypeAlimentaire => ['label' => 'Alimentaire', 'emoji' => '🥘'],
            $shopTypeNonAlimentaire => ['label' => 'Non alimentaire', 'emoji' => '🛍️'],
        ];
        $alimentaire = ['cereales','legumineuses','huiles','snacks','desserts','boissons','condiments','fruits','legumes','conserves','poisson','viandes','miels','epices'];
        $nonAlim = ['cosmetique','electronique','electromenager','mode','chaussures','bagagerie'];
        $sql = 'SELECT * FROM products WHERE is_active = 1';
        $params = [];
        if ($filter_type === $shopTypeAlimentaire) { $sql .= ' AND category IN (' . implode(',', array_fill(0, count($alimentaire), '?')) . ')'; $params = array_merge($params, $alimentaire); }
        elseif ($filter_type === $shopTypeNonAlimentaire) { $sql .= ' AND category IN (' . implode(',', array_fill(0, count($nonAlim), '?')) . ')'; $params = array_merge($params, $nonAlim); }
        if ($filter_cat) { $sql .= ' AND category = ?'; $params[] = $filter_cat; }
        $sql .= ' ORDER BY category ASC, name ASC';
        $products = Database::fetchAll($sql, $params);
        $catalogSections = [];
        if (!$filter_cat && !$filter_type) {
            $grouped = [];
            foreach ($products as $p) $grouped[$p['category']][] = ['kind' => 'product', 'product' => $p];
            foreach ($shopRayons as $key) if (!empty($grouped[$key])) $catalogSections[] = ['key' => $key, 'entries' => $grouped[$key]];
        }
        $catalog = array_map(fn($p) => ['kind' => 'product', 'product' => $p], $products);
        $shopCounts = [];
        foreach ($shopRayons as $key) $shopCounts[$key] = (int) (Database::fetch('SELECT COUNT(*) AS c FROM products WHERE is_active = 1 AND category = ?', [$key])['c'] ?? 0);
        $universeCounts = [
            $shopTypeAlimentaire => array_sum(array_intersect_key($shopCounts, array_flip($alimentaire))),
            $shopTypeNonAlimentaire => array_sum(array_intersect_key($shopCounts, array_flip($nonAlim))),
        ];
        view('shop/boutique', [
            'ep' => 'boutique',
            'page_title' => 'Boutique — Yombal Market',
            'filter_cat' => $filter_cat,
            'filter_type' => $filter_type,
            'filter_viande_famille' => null,
            'viande_familles' => [],
            'catalog_sections' => $catalogSections,
            'catalog' => $catalog,
            'total_products' => (int) (Database::fetch('SELECT COUNT(*) AS c FROM products WHERE is_active = 1')['c'] ?? 0),
            'shop_counts' => $shopCounts,
            'shop_rayons' => $shopRayons,
            'universe_counts' => $universeCounts,
            'shop_universe_labels' => $shopUniverseLabels,
            'extra_css' => '<link rel="stylesheet" href="' . e(asset('css/boutique-market.css')) . '?v=3">',
        ]);
    }

    public static function product(string $slug): void
    {
        $product = Database::fetch('SELECT * FROM products WHERE slug = ? AND is_active = 1', [$slug]);
        if (!$product) { http_response_code(404); view('errors/404', ['ep' => '404', 'page_title' => 'Produit introuvable']); return; }
        $related = Database::fetchAll('SELECT * FROM products WHERE is_active = 1 AND category = ? AND id != ? ORDER BY name ASC LIMIT 4', [$product['category'], $product['id']]);
        view('shop/detail', ['ep' => 'product_detail', 'page_title' => $product['name'] . ' — Yombal Market', 'product' => $product, 'related' => $related, 'extra_css' => '<link rel="stylesheet" href="' . e(asset('css/boutique-market.css')) . '">']);
    }
}
