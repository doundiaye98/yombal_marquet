<?php
$submitted = $submitted ?? false;
$submission = $submission ?? null;
$form_data = $form_data ?? ['first_name' => '', 'last_name' => '', 'email' => '', 'phone' => '', 'message' => '', 'topic_slug' => '', 'consent' => false];
$show_topic_select = $show_topic_select ?? false;
$topic_choices = $topic_choices ?? [];
$topic_select_label = $topic_select_label ?? 'Service concerné';
$form_action = $form_action ?? url('/ecosysteme/' . ($service['slug'] ?? ''));
?>
<section class="section ecosystem-demande-section" id="demande-form" tabindex="-1">
  <div class="ecosystem-demande-wrap ecosystem-demande-wrap--inline">
    <?php if ($submitted && $submission): ?>
    <div class="ecosystem-demande-success" role="status">
      <span class="ecosystem-demande-success__icon" aria-hidden="true">✓</span>
      <h2>Demande envoyée</h2>
      <p>Merci <strong><?= e($submission['name']) ?></strong>, nous avons bien reçu votre demande concernant <strong><?= e($submission['topic_label']) ?></strong>.</p>
      <p>Un accusé de réception a été envoyé à <strong><?= e($submission['email']) ?></strong>.</p>
    </div>
    <?php else: ?>
    <div class="form-panel ecosystem-demande-form ecosystem-demande-form--inline">
      <h2 class="form-panel-title">Votre demande</h2>
      <p class="form-panel-hint">Décrivez votre besoin — réponse sous 24 à 48&nbsp;h ouvrées.</p>
      <form method="post" action="<?= e($form_action) ?>" novalidate>
        <?= csrf_field() ?>
        <?php if ($show_topic_select): ?>
        <div class="field-group">
          <label class="field-label" for="eco_topic"><?= e($topic_select_label) ?> <span aria-hidden="true">*</span></label>
          <select id="eco_topic" class="field-input" name="topic_slug" required>
            <option value="">— Choisir —</option>
            <?php foreach ($topic_choices as $key => $label): ?>
            <option value="<?= e($key) ?>"<?= ($form_data['topic_slug'] ?? '') === $key ? ' selected' : '' ?>><?= e($label) ?></option>
            <?php endforeach; ?>
          </select>
        </div>
        <?php endif; ?>
        <div class="field-row-2">
          <div class="field-group">
            <label class="field-label" for="eco_first_name">Prénom <span aria-hidden="true">*</span></label>
            <input id="eco_first_name" class="field-input" name="first_name" required autocomplete="given-name" value="<?= e($form_data['first_name'] ?? '') ?>">
          </div>
          <div class="field-group">
            <label class="field-label" for="eco_last_name">Nom <span aria-hidden="true">*</span></label>
            <input id="eco_last_name" class="field-input" name="last_name" required autocomplete="family-name" value="<?= e($form_data['last_name'] ?? '') ?>">
          </div>
        </div>
        <div class="field-group">
          <label class="field-label" for="eco_email">E-mail <span aria-hidden="true">*</span></label>
          <input id="eco_email" class="field-input" type="email" name="email" required autocomplete="email" value="<?= e($form_data['email'] ?? '') ?>">
        </div>
        <div class="field-group">
          <label class="field-label" for="eco_phone">Téléphone <span aria-hidden="true">*</span></label>
          <input id="eco_phone" class="field-input" type="tel" name="phone" required autocomplete="tel" placeholder="06 12 34 56 78" value="<?= e($form_data['phone'] ?? '') ?>">
        </div>
        <div class="field-group">
          <label class="field-label" for="eco_message">Votre message <span aria-hidden="true">*</span></label>
          <textarea id="eco_message" class="field-textarea" name="message" rows="5" required placeholder="Précisez dates, lieu, budget ou toute information utile…"><?= e($form_data['message'] ?? '') ?></textarea>
        </div>
        <label class="ecosystem-demande-consent">
          <input type="checkbox" name="consent" value="1" required<?= !empty($form_data['consent']) ? ' checked' : '' ?>>
          <span>J'accepte que mes données soient utilisées pour traiter ma demande et être recontacté(e). <a href="<?= e(url('/mentions-legales')) ?>">Mentions légales</a></span>
        </label>
        <button type="submit" class="btn-primary">Envoyer ma demande</button>
      </form>
    </div>
    <?php endif; ?>
  </div>
</section>
