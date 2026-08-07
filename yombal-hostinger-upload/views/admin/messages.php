<?php require __DIR__ . '/_nav.php'; ?>
<section class="section-block">
  <h1>Messages contact</h1>
  <?php foreach ($messages as $m): ?>
  <article style="border-bottom:1px solid #ddd;padding:1rem 0;opacity:<?= $m['is_read'] ? '.65' : '1' ?>">
    <strong><?= e($m['subject']) ?></strong> — <?= e($m['name']) ?> &lt;<?= e($m['email']) ?>&gt;
    <div><?= nl2br(e($m['message'])) ?></div>
    <small><?= e($m['created_at']) ?></small>
    <?php if (!$m['is_read']): ?>
    <form method="post" action="<?= e(url('/admin/message/' . $m['id'])) ?>" style="display:inline">
      <?= csrf_field() ?>
      <button type="submit" class="xd-btn xd-btn--sm">Marquer lu</button>
    </form>
    <?php endif; ?>
  </article>
  <?php endforeach; ?>
</section>
