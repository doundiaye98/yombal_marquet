<section class="section-block" style="max-width:420px;margin:2rem auto">
  <h1>Inscription</h1>
  <form method="post" action="<?= e(url('/auth/inscription')) ?>">
    <?= csrf_field() ?>
    <label>Nom<input type="text" name="name" autocomplete="name"></label>
    <label>E-mail<input type="email" name="email" required autocomplete="email"></label>
    <label>Mot de passe (6 car. min.)<input type="password" name="password" required minlength="6" autocomplete="new-password"></label>
    <button type="submit" class="xd-btn">Créer mon compte</button>
  </form>
  <p style="margin-top:1rem"><a href="<?= e(url('/auth/connexion')) ?>">Déjà un compte ?</a></p>
</section>
<style>label{display:block;margin:1rem 0}input{width:100%;padding:.5rem;margin-top:.25rem}</style>
