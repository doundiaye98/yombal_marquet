<?php
declare(strict_types=1);

final class EcosystemData
{
    public const FORM_SLUGS = [
        'investissement', 'transport', 'restaurant', 'coiffure',
        'electronique', 'electromenager', 'mode', 'chaussures', 'bagagerie', 'autres-services',
    ];

    public const TOPIC_CHOICES = [
        'investissement' => 'Investissement',
        'transport' => 'Yombal Transports',
        'restaurant' => 'Restaurant & traiteur',
        'coiffure' => 'Coiffure & beauté',
        'electronique' => 'Électronique',
        'electromenager' => 'Électroménager',
        'mode' => 'Habillement',
        'chaussures' => 'Chaussures',
        'bagagerie' => 'Sacs & bagagerie',
        'boutique' => 'Boutique en ligne',
        'autre' => 'Autre demande',
    ];

    public const TRANSPORT_TOPICS = [
        'achat_vehicule' => 'Achats véhicules',
        'vente_vehicule' => 'Vente véhicules',
        'location_voiture' => 'Location voiture',
        'demenagement' => 'Déménagement pro',
        'envoi_colis' => 'Envoi de colis',
    ];

    public static function services(): array
    {
        return [
            'voyages' => [
                'slug' => 'voyages', 'icon' => '✈️', 'title' => 'Yombal Voyages', 'short_label' => 'Voyages',
                'tagline' => 'Agence de voyages TourCom — séjours, circuits et vols',
                'lead' => 'Yombal Voyages (Teranga Voyages) organise vos départs vers l\'Afrique, la Méditerranée et le monde entier : vols, séjours balnéaires, circuits et croisières.',
                'cta_label' => 'Voir les offres voyage', 'boutique_category' => null,
                'external_url' => 'https://www.terangavoyages.com/',
                'bullets' => ['Réservation en ligne sur terangavoyages.com', 'Séjours, circuits et vols vers le Sénégal et l\'Afrique', 'Agence à Paris — 75 rue des Moines, 75017'],
            ],
            'investissement' => [
                'slug' => 'investissement', 'icon' => '📈', 'title' => 'Yombal Investissement Opportunités', 'short_label' => 'Investissement',
                'tagline' => 'Opportunités d\'investissement et projets',
                'lead' => 'Identification d\'opportunités d\'investissement en Afrique et en Europe : commerce, agriculture, distribution et projets structurés pour la diaspora.',
                'cta_label' => 'Explorer les opportunités', 'boutique_category' => null,
                'bullets' => ['Étude de faisabilité et mise en relation', 'Projets agro-alimentaires et distribution', 'Accompagnement diaspora investisseurs', 'Confidentialité et suivi personnalisé'],
            ],
            'immobilier-btp' => ImmobilierData::service(),
            'transport' => [
                'slug' => 'transport', 'icon' => '🚗', 'title' => 'Yombal Transports', 'short_label' => 'Transports',
                'tagline' => 'Véhicules, location, déménagement et envoi de colis',
                'lead' => 'Achat et vente de véhicules, location de voiture, déménagement professionnel et envoi de colis — une offre complète du Groupe YOMBAL.',
                'cta_label' => 'Faire une demande', 'boutique_category' => null,
                'bullets' => ['Achats véhicules', 'Vente véhicules', 'Location voiture', 'Déménagement pro', 'Envoi de colis'],
            ],
            'restaurant' => [
                'slug' => 'restaurant', 'icon' => '🍽️', 'title' => 'Yombal Restaurant', 'short_label' => 'Restaurant',
                'tagline' => 'Restauration et saveurs africaines',
                'lead' => 'Restauration authentique, traiteur et événements autour des saveurs que vous retrouvez aussi dans notre épicerie.',
                'cta_label' => 'Réserver / commander', 'boutique_category' => null,
                'bullets' => ['Plats traditionnels et cuisine du marché', 'Traiteur pour événements et fêtes', 'Carte évolutive selon les saisons', 'Réservations et commandes groupe'],
            ],
            'electronique' => [
                'slug' => 'electronique', 'icon' => '📱', 'title' => 'Yombal Électronique', 'short_label' => 'Électronique',
                'tagline' => 'Smartphones, high-tech et accessoires',
                'lead' => 'Smartphones (iPhone, Samsung et autres marques), multimédia, accessoires et petit high-tech — une offre Yombal Market disponible en boutique en ligne.',
                'cta_label' => 'Voir les produits', 'boutique_category' => 'electronique',
                'bullets' => ['Smartphones et accessoires', 'Écouteurs, enceintes, wearables', 'Commande en ligne et livraison suivie'],
            ],
            'electromenager' => [
                'slug' => 'electromenager', 'icon' => '🏠', 'title' => 'Yombal Électroménager', 'short_label' => 'Électroménager',
                'tagline' => 'Petit électroménager utile au quotidien',
                'lead' => 'Bouilloires, aspirateurs, mixeurs et équipements malins pour la maison.',
                'cta_label' => 'Voir les produits', 'boutique_category' => 'electromenager',
                'bullets' => ['Petit électroménager', 'Maison et confort', 'Livraison selon zone'],
            ],
            'mode' => [
                'slug' => 'mode', 'icon' => '👗', 'title' => 'Yombal Mode', 'short_label' => 'Habillement',
                'tagline' => 'Habillement, tenues du quotidien et pièces diaspora',
                'lead' => 'Une mode accessible, pratique et identitaire — t-shirts, chemises, robes, pagne et sportwear.',
                'cta_label' => 'Voir les produits', 'boutique_category' => 'mode',
                'bullets' => ['T-shirts, chemises, robes', 'Pagne et sportwear', 'Pièces pour toute la famille'],
            ],
            'chaussures' => [
                'slug' => 'chaussures', 'icon' => '👟', 'title' => 'Yombal Chaussures', 'short_label' => 'Chaussures',
                'tagline' => 'Baskets, sandales, ville et enfants',
                'lead' => 'Le bon modèle pour chaque usage — ville, running, sandales, femmes, hommes et enfants.',
                'cta_label' => 'Voir les produits', 'boutique_category' => 'chaussures',
                'bullets' => ['Ville, running, sandales', 'Femmes, hommes, enfants', 'Livraison à domicile'],
            ],
            'bagagerie' => [
                'slug' => 'bagagerie', 'icon' => '🧳', 'title' => 'Yombal Bagagerie', 'short_label' => 'Sacs & bagagerie',
                'tagline' => 'Sacs, valises et accessoires de voyage',
                'lead' => 'Des modèles utiles pour la ville comme pour le départ — sacs urbains, valises et week-enders.',
                'cta_label' => 'Voir les produits', 'boutique_category' => 'bagagerie',
                'bullets' => ['Sacs urbains et scolaires', 'Valises et week-enders', 'Pratiques, solides, stylés'],
            ],
            'coiffure' => [
                'slug' => 'coiffure', 'icon' => '💇', 'title' => 'Yombal Coiffure', 'short_label' => 'Coiffure',
                'tagline' => 'Coiffure afro et soins capillaires',
                'lead' => 'Coiffure afro, soins capillaires et produits naturels (karité, huiles) — sur place ou à domicile selon zone.',
                'cta_label' => 'Prendre rendez-vous', 'boutique_category' => null,
                'bullets' => ['Coiffure afro et soins capillaires', 'Produits naturels (karité, huiles)', 'Rendez-vous sur place ou à domicile (selon zone)', 'Tarifs affichés sur demande'],
            ],
            'autres-services' => [
                'slug' => 'autres-services', 'icon' => '✦', 'title' => 'Autres services', 'short_label' => 'Autres',
                'tagline' => 'Toute l\'offre du Groupe YOMBAL',
                'lead' => 'Découvrez l\'ensemble des prestations du Groupe YOMBAL : boutique en ligne, livraison, conseil et services sur mesure.',
                'cta_label' => 'Nous contacter', 'boutique_category' => null,
                'bullets' => ['Boutique alimentaire, cosmétique, électronique et mode', 'Électroménager, chaussures et bagagerie', 'Immobilier & BTP et investissement', 'Livraison à domicile', 'Contact unique pour toutes vos demandes'],
            ],
        ];
    }

    public static function get(string $slug): ?array
    {
        $all = self::services();
        return $all[$slug] ?? null;
    }

    public static function slideshows(): array
    {
        return [
            'restaurant' => ['img/yombal-restaurant.jpg', 'img/resto-hero.jpg', 'img/resto-1.jpg', 'img/resto-2.jpg', 'img/resto-3.jpg', 'img/resto-4.jpg', 'img/resto-5.jpg', 'img/resto-6.jpg'],
            'electronique' => ['img/yombal-electronique.jpg', 'img/electronics-smartphone-new.jpg', 'img/electronics-accessories-new.jpg', 'img/electronics-earbuds-new.jpg', 'img/electronics-speaker-new.jpg', 'img/electronics-smartwatch-new.jpg'],
            'electromenager' => ['img/yombal-electromenager.jpg', 'img/yombal-electronique-hero-v2.jpg', 'img/gallery-electronique-accessories.jpg', 'img/gallery-electronique-audio.jpg', 'img/gallery-electronique-smartphones.jpg', 'img/gallery-electronique-smarthome.jpg', 'img/gallery-electronique-wearables.jpg'],
            'mode' => ['img/yombal-habillement-hero.jpg', 'img/gallery-habillement-tshirts.jpg', 'img/gallery-habillement-chemises.jpg', 'img/gallery-habillement-robes.jpg', 'img/gallery-habillement-jeans.jpg', 'img/gallery-habillement-sport.jpg', 'img/gallery-habillement-pagne.jpg'],
            'chaussures' => ['img/yombal-chaussures-hero.jpg', 'img/gallery-chaussures-baskets.jpg', 'img/gallery-chaussures-running.jpg', 'img/gallery-chaussures-sandales.jpg', 'img/gallery-chaussures-ville.jpg', 'img/gallery-chaussures-bottes.jpg', 'img/gallery-chaussures-enfants.jpg'],
            'bagagerie' => ['img/bag-backpack.jpg', 'img/bag-suitcase.jpg', 'img/bag-weekender.jpg', 'img/bag-urban.jpg', 'img/bag-crossbody.jpg'],
            'investissement' => ['img/yombal-investissement-opportunites.jpg', 'img/investissement-desk.jpg', 'img/investissement-market.jpg', 'img/investissement-team.jpg', 'img/investissement-partnership.jpg', 'img/investissement-logistics.jpg'],
        ];
    }

    public static function photoBg(string $slug): ?string
    {
        return ['transport' => 'img/yombal-transports.jpg'][$slug] ?? null;
    }

    public static function projectTypes(): array
    {
        return [
            'terrain' => 'Terrain à céder',
            'visite' => 'Visite de site',
            'protocole' => 'Protocole d\'accord',
            'btp' => 'Devis construction / rénovation (BTP)',
            'autre' => 'Autre projet',
        ];
    }
}
