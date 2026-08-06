<section class="section-block">
  <div class="section-head"><h1><?= e($recipe['title']) ?></h1>
  <?php if ($recipe['summary']): ?><p><?= e($recipe['summary']) ?></p><?php endif; ?></div>
  <h2>Ingrédients</h2>
  <ul><?php foreach ($lines as $l): ?><li><a href="<?= e(url('/produit/' . $l['slug'])) ?>"><?= e($l['name']) ?></a> × <?= (int) $l['quantity'] ?></li><?php endforeach; ?></ul>
</section>
