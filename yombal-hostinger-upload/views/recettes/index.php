<section class="section-block">
  <div class="section-head"><h1>Recettes</h1></div>
  <?php if (!$recipes): ?><p>Aucune recette en base pour le moment.</p>
  <?php else: ?><ul><?php foreach ($recipes as $r): ?><li><a href="<?= e(url('/recette/' . $r['slug'])) ?>"><?= e($r['title']) ?></a></li><?php endforeach; ?></ul><?php endif; ?>
</section>
