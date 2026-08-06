<section class="section-block" style="max-width:420px;margin:2rem auto">
  <h1>Admin — Connexion</h1>
  <form method="post" action="<?= e(url('/admin/connexion')) ?>">
    <?= csrf_field() ?>
    <label>E-mail<input type="email" name="email" required></label>
    <label>Mot de passe<input type="password" name="password" required></label>
    <button type="submit" class="xd-btn">Entrer</button>
  </form>
</section>
<style>label{display:block;margin:1rem 0}input{width:100%;padding:.5rem;margin-top:.25rem}</style>
