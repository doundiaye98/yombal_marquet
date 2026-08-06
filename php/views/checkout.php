<?php $est = checkout_delivery_estimate(); ?>
<div class="page-wrapper order-flow-page">
  <?= checkout_steps('checkout') ?>
  <header class="page-hero page-hero--compact">
    <p class="section-eyebrow reveal">Commande</p>
    <h1 class="section-title reveal">Récapitulatif</h1>
    <p class="section-sub reveal">Coordonnées, adresse, puis paiement — <strong>sans compte obligatoire</strong>.</p>
  </header>

  <section class="section section--flush-top">
    <?= order_trust_panel('checkout') ?>
    <div class="cart-summary checkout-summary-box reveal">
      <ul class="checkout-list checkout-list--flush">
        <?php foreach ($items as $row): ?><li class="checkout-line"><span><?= e($row['product']['name']) ?> × <?= (int) $row['quantity'] ?></span><span><?= e(number_format($row['line_total_cents'] / 100, 2, '.', '')) ?> €</span></li><?php endforeach; ?>
        <li class="checkout-line"><span>Sous-total</span><span><?= e(number_format($subtotal_cents / 100, 2, '.', '')) ?> €</span></li>
        <?php if ($shipping_cents): ?><li class="checkout-line"><span>Livraison</span><span><?= e(number_format($shipping_cents / 100, 2, '.', '')) ?> €</span></li><?php elseif (!empty($guest_form['delivery_postal_code'])): ?><li class="checkout-line"><span>Livraison</span><span>Offerte</span></li><?php endif; ?>
        <?php if ($discount_cents): ?><li class="checkout-line"><span>Réduction<?= $promo_code ? ' (' . e($promo_code) . ')' : '' ?></span><span>- <?= e(number_format($discount_cents / 100, 2, '.', '')) ?> €</span></li><?php endif; ?>
        <li class="checkout-line checkout-total"><strong>Total TTC</strong><strong><?= e(number_format($total_cents / 100, 2, '.', '')) ?> €</strong></li>
      </ul>
      <p class="checkout-delivery-estimate">🚚 Livraison estimée : <strong><?= e($est['label']) ?></strong> <span class="muted-small">(<?= (int) $est['days_min'] ?>–<?= (int) $est['days_max'] ?> j. ouvrés)</span></p>
    </div>

    <form method="post" class="checkout-actions reveal">
      <?= csrf_field() ?>
      <?php if (!Auth::check()): ?>
      <div class="form-panel">
        <h2 class="form-panel-title">Coordonnées (sans compte)</h2>
        <p class="form-panel-hint">Pas besoin de créer un compte : indiquez simplement vos coordonnées pour la livraison. Ou <a href="<?= e(url('/auth/connexion?next=' . urlencode('/checkout'))) ?>">connectez-vous</a> / <a href="<?= e(url('/auth/inscription')) ?>">créez un compte</a> pour retrouver vos commandes plus facilement.</p>
        <div class="field-group"><label class="field-label" for="guest_name">Nom complet</label><input id="guest_name" class="field-input" type="text" name="guest_name" required autocomplete="name" value="<?= e($guest_form['guest_name'] ?? '') ?>"></div>
        <div class="field-group"><label class="field-label" for="guest_email">E-mail</label><input id="guest_email" class="field-input" type="email" name="guest_email" required autocomplete="email" value="<?= e($guest_form['guest_email'] ?? '') ?>"></div>
      </div>
      <?php endif; ?>
      <div class="form-panel"><h2 class="form-panel-title">Téléphone</h2><p class="form-panel-hint">Pour la livraison et la confirmation de commande par SMS.</p><div class="field-group"><label class="field-label" for="customer_phone">Numéro de mobile</label><input id="customer_phone" class="field-input" type="tel" name="customer_phone" required autocomplete="tel" placeholder="06 12 34 56 78 ou +221 77 123 45 67" value="<?= e($guest_form['customer_phone'] ?? ($guest_form['guest_phone'] ?? '')) ?>"></div></div>
      <div class="form-panel"><h2 class="form-panel-title">Adresse de livraison</h2><div class="field-group"><label class="field-label" for="delivery_line1">Adresse</label><input id="delivery_line1" class="field-input" type="text" name="delivery_line1" required autocomplete="street-address" value="<?= e($guest_form['delivery_line1'] ?? '') ?>"></div><div class="field-group"><label class="field-label" for="delivery_line2">Complément (facultatif)</label><input id="delivery_line2" class="field-input" type="text" name="delivery_line2" autocomplete="address-line2" value="<?= e($guest_form['delivery_line2'] ?? '') ?>"></div><div class="field-row-2"><div class="field-group"><label class="field-label" for="delivery_postal_code">Code postal</label><input id="delivery_postal_code" class="field-input" type="text" name="delivery_postal_code" required autocomplete="postal-code" value="<?= e($guest_form['delivery_postal_code'] ?? '') ?>"></div><div class="field-group"><label class="field-label" for="delivery_city">Ville</label><input id="delivery_city" class="field-input" type="text" name="delivery_city" required autocomplete="address-level2" value="<?= e($guest_form['delivery_city'] ?? '') ?>"></div></div><div class="field-group"><label class="field-label" for="delivery_country">Pays</label><select id="delivery_country" class="field-input" name="delivery_country" required autocomplete="country"><?php $selectedCountry = $guest_form['delivery_country'] ?? 'FR'; foreach ($delivery_countries as $code => $label): ?><option value="<?= e($code) ?>" <?= $selectedCountry === $code ? 'selected' : '' ?>><?= e($label) ?></option><?php endforeach; ?></select><p class="field-hint">France : tarif selon zone. Autres pays : forfait international.</p></div></div>
      <div class="form-panel"><h2 class="form-panel-title">Code promo (facultatif)</h2><div class="field-group"><label class="field-label" for="promo_code">Code</label><input id="promo_code" class="field-input" type="text" name="promo_code" placeholder="Ex. BIENVENUE10" value="<?= e($promo_code ?: ($guest_form['promo_code'] ?? '')) ?>"></div></div>
      <div class="form-panel"><h2 class="form-panel-title">Notifications</h2><div class="field-group"><label class="checkout-notify-label"><input type="checkbox" name="notify_status_updates" value="1" checked>M’informer par e-mail et SMS des mises à jour (paiement, expédition, livraison)</label></div></div>
      <div class="form-panel"><h2 class="form-panel-title">Cadeau & instructions</h2><div class="field-group"><label><input type="checkbox" name="is_gift" value="1" <?= (($guest_form['is_gift'] ?? '') === '1') ? 'checked' : '' ?>> C'est un cadeau</label></div><div class="field-group"><label class="field-label" for="gift_message">Message cadeau</label><textarea id="gift_message" name="gift_message" rows="2" class="field-textarea" placeholder="Texte pour la carte cadeau…"><?= e($guest_form['gift_message'] ?? '') ?></textarea></div><div class="field-group"><label class="field-label" for="customer_notes">Instructions livreur (facultatif)</label><textarea id="customer_notes" name="customer_notes" rows="3" class="field-textarea" placeholder="Sonnette, gardien, créneau…"><?= e($guest_form['customer_notes'] ?? '') ?></textarea></div></div>
      <div class="checkout-actions-footer"><p class="checkout-pay-reassure">Ensuite : choix du paiement (carte, PayPal, virement ou espèces à la livraison).</p><button type="submit" class="btn-primary">Confirmer et payer</button><a href="<?= e(url('/panier')) ?>" class="btn-outline">Modifier le panier</a></div>
    </form>
  </section>
</div>
