<div class="page-wrapper auth-shell">
  <div class="auth-card reveal">
    <h1>Espace client</h1>
    <p class="auth-lead">Connectez-vous pour suivre vos commandes et retrouver votre historique.</p>
    <form method="post" action="<?= e(url('/auth/connexion' . ($next ? '?next=' . urlencode($next) : ''))) ?>">
      <?= csrf_field() ?>
      <input type="hidden" name="next" value="<?= e($next ?? '') ?>">
      <div class="field-group"><label class="field-label" for="email">E-mail</label><input class="field-input" type="email" id="email" name="email" required autocomplete="email" value="<?= e($old_email ?? '') ?>"></div>
      <div class="field-group"><label class="field-label" for="password">Mot de passe</label><input class="field-input" type="password" id="password" name="password" required autocomplete="current-password"></div>
      <label class="field-check" style="display:flex;align-items:center;gap:8px;margin-bottom:20px;font-size:14px;"><input type="checkbox" name="remember" value="1"> Rester connecté</label>
      <button type="submit" class="btn-primary" style="width:100%;justify-content:center;">Se connecter</button>
      <p class="auth-alt" style="margin-top:20px;font-size:14px;text-align:center;color:var(--text2);">Pas encore de compte ? <a href="<?= e(url('/auth/inscription')) ?>">Créer un compte</a></p>
      <p style="margin-top:16px;font-size:13px;text-align:center;color:var(--text2);"><a href="<?= e(url('/suivi-commande')) ?>">Suivre une commande sans compte →</a></p>
    </form>
  </div>
</div>
