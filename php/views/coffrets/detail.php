<section class="section-block">
  <div class="section-head"><h1><?= e($coffret['title']) ?></h1>
  <?php if ($coffret['summary']): ?><p><?= e($coffret['summary']) ?></p><?php endif; ?></div>
  <ul><?php foreach ($lines as $l): ?><li><a href="<?= e(url('/produit/' . $l['slug'])) ?>"><?= e($l['name']) ?></a> × <?= (int) $l['quantity'] ?></li><?php endforeach; ?></ul>
</section>
