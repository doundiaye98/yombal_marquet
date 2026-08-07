<?php
declare(strict_types=1);

final class ImmobilierData
{
    public static function contact(): array
    {
        return [
            'phone' => '06 31 27 33 76',
            'phone_href' => 'tel:+33631273376',
            'email' => 'imo@universdiaspora.com',
            'address' => '19 rue Richomme, 75018 Paris',
        ];
    }

    public static function program(): array
    {
        return [
            'name' => 'YOMBAL KEUR',
            'tagline' => 'Une cité entièrement dédiée à la diaspora',
            'intro' => 'Le Groupe YOMBAL et Univers Diaspora proposent des terrains à céder au Sénégal, avec paiement échelonné sans apport initial, pour construire votre projet à distance.',
        ];
    }

    public static function service(): array
    {
        return [
            'slug' => 'immobilier-btp',
            'icon' => '🏗️',
            'title' => 'Yombal Immobilier & BTP',
            'short_label' => 'Immobilier & BTP',
            'tagline' => 'Programme YOMBAL KEUR — terrains diaspora & construction',
            'lead' => 'Terrains à céder au Sénégal (Yenne Ndoukhoura Peulh, Sangalcam, Ndayane) avec paiement échelonné sans apport initial, et accompagnement BTP pour vos projets de construction.',
            'cta_label' => 'Demander un projet',
            'boutique_category' => null,
            'bullets' => [
                'Programme YOMBAL KEUR — cité dédiée à la diaspora',
                'Parcelles de 150 m² — paiement échelonné, apport initial 0 €',
                'Titre foncier, acte administratif ou notification de bail selon le site',
                'Visite de site, protocole d\'accord et représentant légal',
                'Construction, rénovation et suivi de chantier (BTP)',
            ],
        ];
    }

    public static function terrains(): array
    {
        $raw = [
            [
                'slug' => 'yenne-ndoukhoura',
                'location' => 'Yenne Ndoukhoura Peulh',
                'country' => 'Sénégal',
                'headline' => 'Opportunité à Yenne Ndoukhoura Peulh',
                'cover' => 'img/immobilier/gemini-terrain.png',
                'cover_alt' => 'Vue du terrain à Yenne Ndoukhoura Peulh — programme YOMBAL KEUR',
                'surface_m2' => 150,
                'price_euros' => 5670,
                'initial_deposit_euros' => 0,
                'monthly_payment_euros' => 189,
                'duration_months' => 30,
                'legal_nature' => 'Acte Administratif',
                'highlights' => [],
                'services' => ['Visite de site', 'Élaboration d\'un protocole d\'accord', 'Représentant légal pour régularisation'],
            ],
            [
                'slug' => 'sangalcam',
                'location' => 'Sangalcam',
                'country' => 'Sénégal',
                'headline' => 'Grande opportunité à Sangalcam',
                'cover' => 'img/immobilier/gemini-chantier-btp.png',
                'cover_alt' => 'Chantier et terrain à Sangalcam — programme YOMBAL KEUR',
                'surface_m2' => 150,
                'price_euros' => 19008,
                'initial_deposit_euros' => 0,
                'monthly_payment_euros' => 396,
                'duration_months' => 48,
                'legal_nature' => 'Titre Foncier',
                'highlights' => ['5 min de la Route Nationale', 'Autorisation de lotir', 'Certificat de conformité'],
                'services' => ['Visite de site', 'Élaboration d\'un protocole d\'accord', 'Représentant légal pour régularisation'],
            ],
            [
                'slug' => 'ndayane',
                'location' => 'Ndayane',
                'country' => 'Sénégal',
                'headline' => 'Grande opportunité à Ndayane',
                'cover' => 'img/immobilier/gemini-terrain.png',
                'cover_alt' => 'Vue du terrain à Ndayane — programme YOMBAL KEUR',
                'surface_m2' => 150,
                'price_euros' => 11960,
                'initial_deposit_euros' => 0,
                'monthly_payment_euros' => 299,
                'duration_months' => 40,
                'legal_nature' => 'Notification de Bail',
                'highlights' => [],
                'services' => ['Visite de site', 'Élaboration d\'un protocole d\'accord', 'Représentant légal pour régularisation'],
            ],
        ];

        foreach ($raw as &$t) {
            $t['price_label'] = self::eur($t['price_euros']);
            $t['monthly_label'] = self::eur($t['monthly_payment_euros']);
            $t['deposit_label'] = self::eur($t['initial_deposit_euros']);
        }
        unset($t);
        return $raw;
    }

    private static function eur(float|int $amount): string
    {
        return number_format((float) $amount, 0, ',', "\u{00a0}") . "\u{00a0}€";
    }
}
