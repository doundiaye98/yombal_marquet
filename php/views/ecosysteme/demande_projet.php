<?php
$form_data = $form_data ?? [
    'first_name' => '', 'last_name' => '', 'email' => '', 'phone' => '', 'country' => '',
    'project_type' => 'terrain', 'terrain_slug' => '', 'message' => '',
];
$project_types = $project_types ?? EcosystemData::projectTypes();
$submitted = $submitted ?? false;
$submission = $submission ?? null;
?>
<div class="page-wrapper immo-page immo-page--demande">
  <header class="immo-demande-hero">
    <div class="immo-demande-hero__inner">
      <a href="<?= e(url('/ecosysteme/immobilier-btp')) ?>" class="immo-demande-hero__back">← Retour aux terrains</a>
      <p class="immo-demande-hero__eyebrow">Groupe YOMBAL · <?= e($program['name']) ?></p>
      <h1 class="immo-demande-hero__title">Demander <em>votre projet</em></h1>
      <p class="immo-demande-hero__lead">Remplissez ce formulaire pour être recontacté : visite de site, protocole d'accord, plan de paiement ou devis BTP. Réponse sous 24 à 48&nbsp;h ouvrées.</p>
    </div>
  </header>

  <div class="immo-demande-layout">
    <aside class="immo-demande-aside" aria-label="Informations utiles">
      <div class="immo-demande-aside__card">
        <h2>Comment ça marche ?</h2>
        <ol class="immo-demande-steps">
          <li><strong>1.</strong> Vous décrivez votre projet</li>
          <li><strong>2.</strong> Un conseiller vous rappelle</li>
          <li><strong>3.</strong> Visite de site &amp; protocole d'accord</li>
          <li><strong>4.</strong> Paiement échelonné &amp; suivi BTP</li>
        </ol>
      </div>
      <div class="immo-demande-aside__card immo-demande-aside__card--contact">
        <h3>Besoin d'aide ?</h3>
        <a href="<?= e($contact['phone_href']) ?>" class="immo-demande-aside__phone"><?= e($contact['phone']) ?></a>
        <a href="mailto:<?= e($contact['email']) ?>" class="email-chip"><?= e($contact['email']) ?></a>
        <p class="immo-demande-aside__addr"><?= e($contact['address']) ?></p>
      </div>
    </aside>

    <div class="immo-demande-main">
      <?php if ($submitted && $submission): ?>
      <div class="immo-demande-success" role="status">
        <span class="immo-demande-success__icon" aria-hidden="true">✓</span>
        <h2>Demande envoyée</h2>
        <p>Merci <strong><?= e($submission['name']) ?></strong>, nous avons bien reçu votre demande concernant <strong><?= e($submission['project_type_label']) ?></strong><?php if (!empty($submission['terrain_label'])): ?> — terrain <strong><?= e($submission['terrain_label']) ?></strong><?php endif; ?>.</p>
        <p>Un accusé de réception a été envoyé à <strong><?= e($submission['email']) ?></strong>.</p>
        <div class="immo-demande-success__actions">
          <a href="<?= e(url('/ecosysteme/immobilier-btp')) ?>" class="btn-primary">Voir les terrains</a>
          <a href="<?= e(url('/')) ?>" class="btn-outline">Retour à l'accueil</a>
        </div>
      </div>
      <?php else: ?>
      <form class="immo-demande-form" method="post" action="<?= e(url('/ecosysteme/immobilier-btp/demande')) ?>" novalidate>
        <?= csrf_field() ?>
        <fieldset class="immo-demande-form__section">
          <legend>Vos coordonnées</legend>
          <div class="field-row-2">
            <div class="field-group">
              <label class="field-label" for="immo_first_name">Prénom <span aria-hidden="true">*</span></label>
              <input id="immo_first_name" class="field-input" name="first_name" required autocomplete="given-name" value="<?= e($form_data['first_name']) ?>">
            </div>
            <div class="field-group">
              <label class="field-label" for="immo_last_name">Nom <span aria-hidden="true">*</span></label>
              <input id="immo_last_name" class="field-input" name="last_name" required autocomplete="family-name" value="<?= e($form_data['last_name']) ?>">
            </div>
          </div>
          <div class="field-row-2">
            <div class="field-group">
              <label class="field-label" for="immo_email">E-mail <span aria-hidden="true">*</span></label>
              <input id="immo_email" class="field-input" type="email" name="email" required autocomplete="email" value="<?= e($form_data['email']) ?>">
            </div>
            <div class="field-group">
              <label class="field-label" for="immo_phone">Téléphone <span aria-hidden="true">*</span></label>
              <input id="immo_phone" class="field-input" type="tel" name="phone" required autocomplete="tel" placeholder="06 12 34 56 78" value="<?= e($form_data['phone']) ?>">
            </div>
          </div>
          <div class="field-group">
            <label class="field-label" for="immo_country">Pays de résidence <span aria-hidden="true">*</span></label>
            <input id="immo_country" class="field-input" name="country" required autocomplete="country-name" placeholder="France, Sénégal…" value="<?= e($form_data['country']) ?>">
          </div>
        </fieldset>
        <fieldset class="immo-demande-form__section">
          <legend>Votre projet</legend>
          <div class="field-group">
            <label class="field-label" for="immo_project_type">Type de demande <span aria-hidden="true">*</span></label>
            <select id="immo_project_type" class="field-input" name="project_type" required>
              <?php foreach ($project_types as $key => $label): ?>
              <option value="<?= e($key) ?>"<?= ($form_data['project_type'] ?? '') === $key ? ' selected' : '' ?>><?= e($label) ?></option>
              <?php endforeach; ?>
            </select>
          </div>
          <div class="field-group">
            <label class="field-label" for="immo_terrain">Terrain concerné</label>
            <select id="immo_terrain" class="field-input" name="terrain_slug">
              <option value="">— Je ne sais pas encore / autre —</option>
              <?php foreach ($terrains as $terrain): ?>
              <option value="<?= e($terrain['slug']) ?>"<?= ($form_data['terrain_slug'] ?? '') === $terrain['slug'] ? ' selected' : '' ?>>
                <?= e($terrain['location']) ?> — <?= e($terrain['price_label']) ?> (<?= e($terrain['monthly_label']) ?>/mois)
              </option>
              <?php endforeach; ?>
            </select>
          </div>
          <div class="field-group">
            <label class="field-label" for="immo_message">Message complémentaire</label>
            <textarea id="immo_message" class="field-textarea" name="message" rows="5" placeholder="Précisez votre budget, vos délais, si vous avez un représentant légal au Sénégal…"><?= e($form_data['message']) ?></textarea>
          </div>
        </fieldset>
        <label class="immo-demande-consent">
          <input type="checkbox" name="consent" value="1" required>
          <span>J'accepte que mes données soient utilisées pour traiter ma demande et être recontacté(e) par l'équipe YOMBAL / Univers Diaspora. <a href="<?= e(url('/mentions-legales')) ?>">Mentions légales</a></span>
        </label>
        <button type="submit" class="btn-primary immo-demande-form__submit">Envoyer ma demande</button>
      </form>
      <?php endif; ?>
    </div>
  </div>
</div>
