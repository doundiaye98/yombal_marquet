<?php
declare(strict_types=1);

/**
 * Conseiller boutique — mode local (intentions + recherche produits).
 * Compatible avec le widget Flask (answer, sources, hint, mode, lang).
 */
final class Assistant
{
    public static function enabled(): bool
    {
        return env('ASSISTANT_ENABLED', '1') === '1';
    }

    public static function ready(): bool
    {
        return self::enabled();
    }

    public static function answer(string $question): array
    {
        $q = trim(mb_strtolower($question));
        $q = preg_replace('/\s+/u', ' ', $q) ?? $q;
        if ($q === '') {
            return ['answer' => 'Indiquez votre question concernant nos produits, livraisons ou services.', 'sources' => [], 'lang' => 'fr'];
        }

        if (preg_match('/\b(suivre|suivi)\s+(ma\s+|de\s+la\s+|d[\' ]une?\s+)?commande\b|\bo[uù]\s+en\s+est\s+ma\s+commande\b|\bnuméro\s+de\s+commande\b|\btracking\b|\bstatut\s+(de\s+)?(ma\s+|la\s+)?commande\b/u', $q)) {
            return [
                'answer' => "Pour suivre votre commande, utilisez la page Suivi de commande avec votre numéro et l'e-mail utilisé lors de l'achat.\n\nBesoin d'aide ? Contactez-nous via la page Contact.",
                'sources' => [],
                'hint' => 'order_tracking',
                'lang' => 'fr',
                'mode' => 'local',
            ];
        }

        if (preg_match('/^(bonjour|bonsoir|salut|hello|hi|salam|as-salam)\b/u', $q) || in_array($q, ['merci', 'ok', 'd\'accord'], true)) {
            return [
                'answer' => "Bonjour ! Je suis le conseiller Yombal Market. Posez-moi une question sur la boutique, la livraison ou un service du Groupe YOMBAL (Immobilier, Voyages, Transports…).",
                'sources' => [],
                'hint' => 'greeting',
                'mode' => 'courtesy',
                'lang' => 'fr',
            ];
        }

        if (preg_match('/\bgroupe\s+yombal\b|\bunivers\s+yombal\b|\btous?\s+(vos|les)\s+services\b|\bquels?\s+services\b|\bque\s+proposez/u', $q)) {
            $lines = ["Le Groupe YOMBAL regroupe plusieurs univers :\n"];
            $sources = [];
            foreach (ecosystem_hub_services() as $item) {
                $lines[] = '• ' . $item['short_label'] . ' — ' . ($item['tagline'] ?? '');
                $href = !empty($item['external_url']) ? $item['external_url'] : url('/ecosysteme/' . $item['slug']);
                $sources[] = ['title' => $item['short_label'], 'url' => $href];
            }
            $lines[] = "\nConsultez Univers YOMBAL pour le détail de chaque service.";
            $sources[] = ['title' => 'Univers YOMBAL', 'url' => url('/ecosysteme')];
            return [
                'answer' => implode("\n", $lines),
                'sources' => $sources,
                'hint' => 'ecosystem',
                'mode' => 'local',
                'lang' => 'fr',
            ];
        }

        $ecoIntent = self::matchEcosystem($q);
        if ($ecoIntent) {
            $svc = EcosystemData::get($ecoIntent);
            if ($svc) {
                $url = !empty($svc['external_url']) ? $svc['external_url'] : url('/ecosysteme/' . $svc['slug']);
                $bullets = implode("\n", array_map(fn ($b) => '• ' . $b, $svc['bullets'] ?? []));
                return [
                    'answer' => $svc['title'] . "\n\n" . $svc['lead'] . "\n\n" . $bullets . "\n\nPour une demande personnalisée, utilisez le formulaire sur la page du service.",
                    'sources' => [['title' => $svc['short_label'], 'url' => $url]],
                    'hint' => 'ecosystem',
                    'mode' => 'local',
                    'lang' => 'fr',
                ];
            }
        }

        // Recherche produits
        $terms = array_values(array_filter(preg_split('/\s+/u', $q) ?: [], fn ($t) => mb_strlen($t) >= 3));
        $products = [];
        if ($terms) {
            $like = '%' . $terms[0] . '%';
            try {
                $products = Database::fetchAll(
                    'SELECT name, slug, price_cents, category, stock_qty FROM products WHERE is_active = 1 AND (name LIKE ? OR description LIKE ? OR category LIKE ?) ORDER BY name ASC LIMIT 6',
                    [$like, $like, $like]
                );
            } catch (Throwable) {
                $products = [];
            }
        }

        if ($products) {
            $lines = ["Voici des produits qui correspondent à votre recherche :\n"];
            $sources = [];
            foreach ($products as $p) {
                $price = number_format(((int) $p['price_cents']) / 100, 2, '.', '') . ' €';
                $stock = ((int) ($p['stock_qty'] ?? 0)) > 0 ? 'en stock' : 'stock limité';
                $lines[] = '• ' . $p['name'] . ' — ' . $price . ' (' . $stock . ')';
                $sources[] = ['title' => $p['name'], 'url' => url('/produit/' . $p['slug'])];
            }
            $lines[] = "\nParcourez aussi la boutique complète pour plus de références.";
            $sources[] = ['title' => 'Boutique', 'url' => url('/boutique')];
            return ['answer' => implode("\n", $lines), 'sources' => $sources, 'mode' => 'local', 'lang' => 'fr'];
        }

        if (preg_match('/\b(livraison|délai|frais\s+de\s+port|expédition)\b/u', $q)) {
            $est = checkout_delivery_estimate();
            return [
                'answer' => "Livraison à domicile sous " . $est['label'] . " selon votre zone.\n\nLe montant des frais de port est calculé au panier / checkout. Pour l'international, des frais supplémentaires peuvent s'appliquer.",
                'sources' => [['title' => 'Boutique', 'url' => url('/boutique')], ['title' => 'Contact', 'url' => url('/contact')]],
                'mode' => 'local',
                'lang' => 'fr',
            ];
        }

        if (preg_match('/\b(paiement|payer|carte|stripe|paypal|virement)\b/u', $q)) {
            return [
                'answer' => "Modes de paiement acceptés :\n• Carte bancaire (Stripe)\n• PayPal\n• Virement bancaire\n• Espèces à la livraison (selon zone)\n\nVous choisissez le mode au moment du paiement.",
                'sources' => [['title' => 'Contact & paiement', 'url' => url('/contact')]],
                'mode' => 'local',
                'lang' => 'fr',
            ];
        }

        return [
            'answer' => "Je n'ai pas trouvé d'information précise sur cette question.\n\nEssayez :\n• un nom de produit (riz, iPhone, mixeur…)\n• un service (terrain, voyage, transport…)\n• ou la page Contact pour parler à l'équipe.",
            'sources' => [
                ['title' => 'Boutique', 'url' => url('/boutique')],
                ['title' => 'Univers YOMBAL', 'url' => url('/ecosysteme')],
                ['title' => 'Contact', 'url' => url('/contact')],
            ],
            'mode' => 'local',
            'lang' => 'fr',
        ];
    }

    private static function matchEcosystem(string $q): ?string
    {
        $map = [
            'voyages' => '/\bvoyag|\bvol\b|\bavion\b|\bbillet|\bs[eé]jour|\bcircuit|\bteranga/u',
            'investissement' => '/\binvest|\bopportunit|\bplacement\b|\bfaisabilit/u',
            'immobilier-btp' => '/\bimmobilier|\bterrain|\bparcelle|\bconstruction|\br[eé]novation|\bbtp\b|\bkeur\b|\bndayane|\bsangalcam|\byenne/u',
            'transport' => '/\btransport|\blocation\s+(de\s+)?voiture|\bv[eé]hicule|\bd[eé]m[eé]nagement|\benvoi\s+de\s+colis/u',
            'restaurant' => '/\brestaurant|\btraiteur|\bmanger\b|\bcatering/u',
            'electronique' => '/\b[eé]lectronique|\bsmartphone|\biphone|\bsamsung|\bécouteur|\bcasque|\benceinte/u',
            'electromenager' => '/\b[eé]lectrom[eé]nager|\bmixeur|\bfriteuse|\bbouilloire|\baspirateur/u',
            'mode' => '/\bhabillement|\bv[eê]tement|\bboubou|\bpagne|\brobe|\bchemise|\bt-?shirt/u',
            'chaussures' => '/\bchaussure|\bbasket|\bsandale|\bbotte/u',
            'bagagerie' => '/\bbagagerie|\bvalise|\bsac\b|\bweek-?end/u',
            'coiffure' => '/\bcoiffure|\bcheveux|\bafro|\bkarit/u',
        ];
        foreach ($map as $slug => $re) {
            if (preg_match($re, $q)) {
                return $slug;
            }
        }
        return null;
    }
}
