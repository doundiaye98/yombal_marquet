<section class="section-block">
  <div class="section-head"><h1>Carte des saveurs</h1></div>
  <?php if (!$producers): ?>
  <p>Les producteurs apparaîtront ici une fois importés en base.</p>
  <?php else: ?>
  <ul>
    <?php foreach ($producers as $pr): ?>
    <li><strong><?= e($pr['name']) ?></strong><?= $pr['region'] ? ' — ' . e($pr['region']) : '' ?></li>
    <?php endforeach; ?>
  </ul>
  <?php endif; ?>
</section>
