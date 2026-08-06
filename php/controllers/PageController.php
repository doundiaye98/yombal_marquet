<?php
declare(strict_types=1);

final class PageController
{
    public static function apropos(): void
    {
        $products = (int) (Database::fetch('SELECT COUNT(*) AS c FROM products WHERE is_active = 1')['c'] ?? 0);
        view('apropos', [
            'ep' => 'apropos',
            'page_title' => 'À propos — Yombal Marché',
            'stats' => ['products' => $products, 'rayons' => count(category_labels())],
        ]);
    }

    public static function contact(): void
    {
        $agencies = [
            [
                'id' => 'paris18',
                'label' => 'Agence 1',
                'title' => 'Paris 18e',
                'address_line1' => '57 rue Letort',
                'address_line2' => '75018 Paris',
                'phone_fixe' => '01 42 52 23 23',
                'phone_mobile' => '07 58 86 44 31',
                'maps_link' => 'https://maps.google.com/?q=57+rue+Letort+75018+Paris',
                'maps_embed' => 'https://www.google.com/maps?q=57+rue+Letort+75018+Paris&output=embed',
                'transit' => [['mode' => 'Métro', 'lines' => 'Ligne 4', 'stops' => 'Porte de Clignancourt'], ['mode' => 'Bus', 'lines' => '56 · 255', 'stops' => 'Porte de Clignancourt']],
            ],
            [
                'id' => 'paris17',
                'label' => 'Agence 2',
                'title' => 'Paris 17e',
                'address_line1' => '78 avenue de Clichy',
                'address_line2' => '75017 Paris',
                'phone_fixe' => '01 44 85 14 00',
                'phone_mobile' => '06 95 04 83 06',
                'maps_link' => 'https://maps.google.com/?q=78+avenue+de+Clichy+75017+Paris',
                'maps_embed' => 'https://www.google.com/maps?q=78+avenue+de+Clichy+75017+Paris&output=embed',
                'transit' => [['mode' => 'Métro', 'lines' => 'Ligne 13', 'stops' => 'La Fourche'], ['mode' => 'Bus', 'lines' => '54 · 74', 'stops' => 'Brochant - Cardinet']],
            ],
            [
                'id' => 'colombes',
                'label' => 'Agence 3',
                'title' => 'Colombes',
                'address_line1' => '25 rue Saint-Denis',
                'address_line2' => '92700 Colombes',
                'phone_fixe' => '01 47 85 91 66',
                'phone_mobile' => '07 49 53 31 78',
                'maps_link' => 'https://maps.google.com/?q=25+rue+Saint-Denis+92700+Colombes',
                'maps_embed' => 'https://www.google.com/maps?q=25+rue+Saint-Denis+92700+Colombes&output=embed',
                'transit' => [['mode' => 'Train', 'lines' => 'Ligne J', 'stops' => 'Colombes'], ['mode' => 'Bus', 'lines' => '176 · 304', 'stops' => 'Mairie de Colombes']],
            ],
        ];
        if (is_post()) {
            verify_csrf();
            $name = trim(($_POST['first_name'] ?? '') . ' ' . ($_POST['last_name'] ?? ''));
            if ($name === ' ') {
                $name = trim($_POST['name'] ?? '');
            }
            $email = strtolower(trim($_POST['email'] ?? ''));
            $subject = trim($_POST['subject'] ?? '');
            $message = trim($_POST['message'] ?? '');
            if ($name === '' || !str_contains($email, '@') || strlen($subject) < 3 || strlen($message) < 10) {
                flash('Veuillez remplir tous les champs du formulaire.', 'danger');
            } else {
                Database::insert('contact_messages', [
                    'name' => $name,
                    'email' => $email,
                    'subject' => $subject,
                    'message' => $message,
                    'is_read' => 0,
                ]);
                $to = env('CONTACT_EMAIL', 'compta@universdiasporas.com');
                Mailer::send($to, "[Contact] {$subject}", "De: {$name} <{$email}>\n\n{$message}");
                flash('Message envoyé — nous vous répondrons rapidement.', 'success');
                redirect('/contact');
            }
        }
        $faq = Database::fetchAll(
            'SELECT * FROM faq_items WHERE is_active = 1 ORDER BY sort_order ASC, id ASC'
        );
        view('contact', [
            'ep' => 'contact',
            'page_title' => 'Contact — Yombal Marché',
            'faq_items' => $faq,
            'agencies' => $agencies,
            'agencies_email' => 'agences@universdiasporas.com',
        ]);
    }

    public static function services(): void
    {
        view('services', ['ep' => 'services', 'page_title' => 'Services']);
    }

    public static function decouvrir(): void
    {
        view('decouvrir', ['ep' => 'decouvrir', 'page_title' => 'Découvrir — Yombal Marché']);
    }

    public static function saveurs(): void
    {
        $producers = Database::fetchAll('SELECT * FROM producers WHERE is_active = 1 ORDER BY name ASC');
        view('saveurs', [
            'ep' => 'saveurs',
            'page_title' => 'Carte des saveurs',
            'producers' => $producers,
        ]);
    }

    public static function recettes(): void
    {
        $recipes = Database::fetchAll('SELECT * FROM recipes WHERE is_active = 1 ORDER BY title ASC');
        view('recettes/index', ['ep' => 'recettes', 'page_title' => 'Recettes', 'recipes' => $recipes]);
    }

    public static function recette(string $slug): void
    {
        $recipe = Database::fetch('SELECT * FROM recipes WHERE slug = ? AND is_active = 1', [$slug]);
        if (!$recipe) {
            http_response_code(404);
            view('errors/404', ['ep' => '404', 'page_title' => 'Introuvable']);
            return;
        }
        $lines = Database::fetchAll(
            'SELECT rl.*, p.name, p.slug, p.price_cents, p.image FROM recipe_lines rl
             JOIN products p ON p.id = rl.product_id WHERE rl.recipe_id = ?',
            [(int) $recipe['id']]
        );
        view('recettes/detail', [
            'ep' => 'recette_detail',
            'page_title' => $recipe['title'],
            'recipe' => $recipe,
            'lines' => $lines,
        ]);
    }

    public static function coffrets(): void
    {
        $coffrets = Database::fetchAll('SELECT * FROM coffrets WHERE is_active = 1 ORDER BY title ASC');
        view('coffrets/index', ['ep' => 'coffrets', 'page_title' => 'Coffrets', 'coffrets' => $coffrets]);
    }

    public static function coffret(string $slug): void
    {
        $c = Database::fetch('SELECT * FROM coffrets WHERE slug = ? AND is_active = 1', [$slug]);
        if (!$c) {
            http_response_code(404);
            view('errors/404', ['ep' => '404', 'page_title' => 'Introuvable']);
            return;
        }
        $lines = Database::fetchAll(
            'SELECT cl.*, p.name, p.slug, p.price_cents, p.image FROM coffret_lines cl
             JOIN products p ON p.id = cl.product_id WHERE cl.coffret_id = ?',
            [(int) $c['id']]
        );
        view('coffrets/detail', [
            'ep' => 'coffret_detail',
            'page_title' => $c['title'],
            'coffret' => $c,
            'lines' => $lines,
        ]);
    }

    public static function ecosystemeHub(): void
    {
        self::renderEcosystemePage('autres-services');
    }

    public static function ecosysteme(string $slug): void
    {
        $aliases = ['immobilier' => 'immobilier-btp', 'btp' => 'immobilier-btp'];
        if (isset($aliases[$slug])) {
            redirect('/ecosysteme/' . $aliases[$slug]);
        }
        self::renderEcosystemePage($slug);
    }

    public static function immoDemande(): void
    {
        $program = ImmobilierData::program();
        $terrains = ImmobilierData::terrains();
        $contact = ImmobilierData::contact();
        $projectTypes = EcosystemData::projectTypes();
        $form = [
            'first_name' => '', 'last_name' => '', 'email' => '', 'phone' => '', 'country' => '',
            'project_type' => 'terrain', 'terrain_slug' => trim($_GET['terrain'] ?? ''), 'message' => '',
        ];
        $submitted = false;
        $submission = null;

        if (is_post()) {
            verify_csrf();
            $form['first_name'] = trim($_POST['first_name'] ?? '');
            $form['last_name'] = trim($_POST['last_name'] ?? '');
            $form['email'] = strtolower(trim($_POST['email'] ?? ''));
            $form['phone'] = trim($_POST['phone'] ?? '');
            $form['country'] = trim($_POST['country'] ?? '');
            $form['project_type'] = trim($_POST['project_type'] ?? '');
            $form['terrain_slug'] = trim($_POST['terrain_slug'] ?? '');
            $form['message'] = trim($_POST['message'] ?? '');
            $consent = ($_POST['consent'] ?? '') === '1';
            $errors = [];
            $name = trim($form['first_name'] . ' ' . $form['last_name']);
            if ($name === '' || mb_strlen($form['first_name']) < 2) {
                $errors[] = 'Indiquez votre prénom et nom.';
            }
            if (!str_contains($form['email'], '@')) {
                $errors[] = 'Indiquez une adresse e-mail valide.';
            }
            if (mb_strlen($form['phone']) < 8) {
                $errors[] = 'Indiquez un numéro de téléphone joignable.';
            }
            if ($form['country'] === '') {
                $errors[] = 'Indiquez votre pays de résidence.';
            }
            if (!isset($projectTypes[$form['project_type']])) {
                $errors[] = 'Choisissez un type de demande.';
            }
            if (!$consent) {
                $errors[] = 'Veuillez accepter le traitement de vos données.';
            }
            $terrainLabel = null;
            foreach ($terrains as $t) {
                if ($t['slug'] === $form['terrain_slug']) {
                    $terrainLabel = $t['location'];
                    break;
                }
            }
            if ($errors) {
                foreach ($errors as $err) {
                    flash($err, 'danger');
                }
            } else {
                $typeLabel = $projectTypes[$form['project_type']];
                $body = "Demande Immobilier & BTP\nNom: {$name}\nEmail: {$form['email']}\nTél: {$form['phone']}\nPays: {$form['country']}\nType: {$typeLabel}\nTerrain: " . ($terrainLabel ?: 'non précisé') . "\n\n{$form['message']}";
                Database::insert('contact_messages', [
                    'name' => $name,
                    'email' => $form['email'],
                    'subject' => '[Immobilier] ' . $typeLabel,
                    'message' => $body,
                    'is_read' => 0,
                ]);
                $to = env('CONTACT_EMAIL', 'compta@universdiasporas.com');
                Mailer::send($to, '[Immobilier] ' . $typeLabel . ' — ' . $name, $body);
                Mailer::send($form['email'], 'Accusé de réception — YOMBAL KEUR', "Bonjour {$name},\n\nNous avons bien reçu votre demande concernant {$typeLabel}. Notre équipe vous recontacte sous 24 à 48 h ouvrées.\n\nGroupe YOMBAL");
                $submitted = true;
                $submission = [
                    'name' => $name,
                    'email' => $form['email'],
                    'project_type_label' => $typeLabel,
                    'terrain_label' => $terrainLabel,
                ];
            }
        }

        view('ecosysteme/demande_projet', [
            'ep' => 'ecosysteme_detail',
            'page_title' => 'Demander un projet — ' . $program['name'],
            'main_class' => 'site-main--immo',
            'extra_css' => '<link rel="stylesheet" href="' . e(asset('css/immo-page.css')) . '">',
            'program' => $program,
            'terrains' => $terrains,
            'contact' => $contact,
            'project_types' => $projectTypes,
            'form_data' => $form,
            'submitted' => $submitted,
            'submission' => $submission,
        ]);
    }

    public static function apiAssistant(): void
    {
        header('Content-Type: application/json; charset=utf-8');
        if (!Assistant::enabled()) {
            http_response_code(503);
            echo json_encode(['error' => 'assistant_disabled', 'answer' => 'Le conseiller est temporairement indisponible.'], JSON_UNESCAPED_UNICODE);
            exit;
        }
        $raw = file_get_contents('php://input') ?: '';
        $payload = json_decode($raw, true);
        if (!is_array($payload)) {
            $payload = $_POST;
        }
        $question = trim((string) ($payload['question'] ?? ''));
        if ($question === '') {
            http_response_code(400);
            echo json_encode(['error' => 'question_required', 'answer' => 'Question vide.'], JSON_UNESCAPED_UNICODE);
            exit;
        }
        if (mb_strlen($question) > 500) {
            $question = mb_substr($question, 0, 500);
        }
        echo json_encode(Assistant::answer($question), JSON_UNESCAPED_UNICODE);
        exit;
    }

    private static function renderEcosystemePage(string $slug): void
    {
        if ($slug === 'voyages') {
            redirect('https://www.terangavoyages.com/');
        }

        if ($slug === 'immobilier-btp') {
            $service = ImmobilierData::service();
            view('ecosysteme/immobilier_btp', [
                'ep' => 'ecosysteme_detail',
                'page_title' => $service['title'] . ' — Groupe YOMBAL',
                'main_class' => 'site-main--immo',
                'extra_css' => '<link rel="stylesheet" href="' . e(asset('css/immo-page.css')) . '">',
                'service' => $service,
                'program' => ImmobilierData::program(),
                'terrains' => ImmobilierData::terrains(),
                'contact' => ImmobilierData::contact(),
            ]);
            return;
        }

        $service = EcosystemData::get($slug);
        if (!$service) {
            http_response_code(404);
            view('errors/404', ['ep' => '404', 'page_title' => 'Introuvable']);
            return;
        }

        $formData = [
            'first_name' => '', 'last_name' => '', 'email' => '', 'phone' => '',
            'message' => '', 'topic_slug' => '', 'consent' => false,
        ];
        $submitted = false;
        $submission = null;
        $hasForm = in_array($slug, EcosystemData::FORM_SLUGS, true);

        if ($hasForm && is_post()) {
            verify_csrf();
            $formData['first_name'] = trim($_POST['first_name'] ?? '');
            $formData['last_name'] = trim($_POST['last_name'] ?? '');
            $formData['email'] = strtolower(trim($_POST['email'] ?? ''));
            $formData['phone'] = trim($_POST['phone'] ?? '');
            $formData['message'] = trim($_POST['message'] ?? '');
            $formData['topic_slug'] = trim($_POST['topic_slug'] ?? '');
            $formData['consent'] = ($_POST['consent'] ?? '') === '1';
            $name = trim($formData['first_name'] . ' ' . $formData['last_name']);
            $errors = [];
            if ($slug === 'autres-services') {
                if (!isset(EcosystemData::TOPIC_CHOICES[$formData['topic_slug']])) {
                    $errors[] = 'Choisissez le service concerné.';
                }
                $topicLabel = EcosystemData::TOPIC_CHOICES[$formData['topic_slug']] ?? $service['title'];
            } elseif ($slug === 'transport') {
                if (!isset(EcosystemData::TRANSPORT_TOPICS[$formData['topic_slug']])) {
                    $errors[] = 'Choisissez le type de demande.';
                }
                $topicLabel = $service['title'] . ' — ' . (EcosystemData::TRANSPORT_TOPICS[$formData['topic_slug']] ?? '');
            } else {
                $topicLabel = $service['title'];
            }
            if ($name === '' || mb_strlen($formData['first_name']) < 2) {
                $errors[] = 'Indiquez votre prénom et nom.';
            }
            if (!str_contains($formData['email'], '@')) {
                $errors[] = 'Indiquez une adresse e-mail valide.';
            }
            if (mb_strlen($formData['phone']) < 8) {
                $errors[] = 'Indiquez un numéro de téléphone joignable.';
            }
            if (mb_strlen($formData['message']) < 10) {
                $errors[] = 'Décrivez votre demande (au moins 10 caractères).';
            }
            if (!$formData['consent']) {
                $errors[] = 'Veuillez accepter le traitement de vos données.';
            }
            if ($errors) {
                foreach ($errors as $err) {
                    flash($err, 'danger');
                }
            } else {
                $body = "Demande Univers YOMBAL — {$topicLabel}\nNom: {$name}\nEmail: {$formData['email']}\nTél: {$formData['phone']}\n\n{$formData['message']}";
                Database::insert('contact_messages', [
                    'name' => $name,
                    'email' => $formData['email'],
                    'subject' => '[Écosystème] ' . $topicLabel,
                    'message' => $body,
                    'is_read' => 0,
                ]);
                $to = env('CONTACT_EMAIL', 'compta@universdiasporas.com');
                Mailer::send($to, '[Écosystème] ' . $topicLabel . ' — ' . $name, $body);
                Mailer::send($formData['email'], 'Accusé de réception — Groupe YOMBAL', "Bonjour {$name},\n\nNous avons bien reçu votre demande concernant {$topicLabel}. Réponse sous 24 à 48 h ouvrées.\n\nGroupe YOMBAL");
                $submitted = true;
                $submission = ['name' => $name, 'email' => $formData['email'], 'topic_label' => $topicLabel];
            }
        }

        $products = [];
        if (!empty($service['boutique_category'])) {
            $products = Database::fetchAll(
                'SELECT * FROM products WHERE is_active = 1 AND category = ? ORDER BY name ASC LIMIT 48',
                [$service['boutique_category']]
            );
        }

        $showTopic = $slug === 'autres-services' || $slug === 'transport';
        $topicChoices = $slug === 'transport' ? EcosystemData::TRANSPORT_TOPICS : EcosystemData::TOPIC_CHOICES;
        $extraCss = $products ? '<link rel="stylesheet" href="' . e(asset('css/boutique-market.css')) . '">' : '';

        view('ecosysteme', [
            'ep' => 'ecosysteme_detail',
            'page_title' => ($slug === 'autres-services' ? 'Univers YOMBAL' : $service['title']) . ' — Groupe YOMBAL',
            'slug' => $slug,
            'service' => $service,
            'products' => $products,
            'boutique_products' => $products,
            'extra_css' => $extraCss,
            'form_data' => $formData,
            'submitted' => $submitted,
            'submission' => $submission,
            'show_topic_select' => $showTopic,
            'topic_choices' => $topicChoices,
            'topic_select_label' => $slug === 'transport' ? 'Type de demande' : 'Service concerné',
            'form_action' => url($slug === 'autres-services' ? '/ecosysteme' : '/ecosysteme/' . $slug),
        ]);
    }

    public static function mentions(): void
    {
        view('legal/mentions', ['ep' => 'mentions_legales', 'page_title' => 'Mentions légales']);
    }

    public static function cgv(): void
    {
        view('legal/cgv', ['ep' => 'cgv', 'page_title' => 'CGV']);
    }

    public static function healthz(): void
    {
        header('Content-Type: text/plain; charset=utf-8');
        echo 'ok';
        exit;
    }

    public static function robots(): void
    {
        header('Content-Type: text/plain; charset=utf-8');
        echo "User-agent: *\nAllow: /\nSitemap: " . url('/sitemap.xml') . "\n";
        exit;
    }

    public static function sitemap(): void
    {
        header('Content-Type: application/xml; charset=utf-8');
        $urls = ['/', '/boutique', '/apropos', '/contact', '/cgv', '/mentions-legales'];
        $products = Database::fetchAll('SELECT slug, updated_at FROM products WHERE is_active = 1');
        echo '<?xml version="1.0" encoding="UTF-8"?>';
        echo '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">';
        foreach ($urls as $u) {
            echo '<url><loc>' . e(url($u)) . '</loc></url>';
        }
        foreach ($products as $p) {
            echo '<url><loc>' . e(url('/produit/' . $p['slug'])) . '</loc></url>';
        }
        echo '</urlset>';
        exit;
    }

    public static function manifest(): void
    {
        $file = PHP_ROOT . '/public/static/manifest.webmanifest';
        if (is_file($file)) {
            header('Content-Type: application/manifest+json');
            readfile($file);
            exit;
        }
        http_response_code(404);
        exit;
    }

    public static function sw(): void
    {
        $file = PHP_ROOT . '/public/static/sw.js';
        if (is_file($file)) {
            header('Content-Type: application/javascript');
            header('Service-Worker-Allowed: /');
            readfile($file);
            exit;
        }
        http_response_code(404);
        exit;
    }
}
