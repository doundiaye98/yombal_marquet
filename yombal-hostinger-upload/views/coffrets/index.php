<section class="section-block">
  <div class="section-head"><h1>Coffrets cadeaux</h1></div>
  <?php if (!$coffrets): ?><p>Aucun coffret en base pour le moment.</p>
  <?php else: ?><ul><?php foreach ($coffrets as $c): ?><li><a href="<?= e(url('/coffret/' . $c['slug'])) ?>"><?= e($c['title']) ?></a></li><?php endforeach; ?></ul><?php endif; ?>
</section>
