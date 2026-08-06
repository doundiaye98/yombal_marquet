<?php require __DIR__ . '/_nav.php'; ?>
<section class="section-block">
  <h1><?= e($order['public_ref']) ?></h1>
  <p><?= e(order_status_label($order['status'])) ?> — <?= e(money_eur((int) $order['total_cents'])) ?></p>
  <p>Client : <?= e($order['guest_name'] ?: '—') ?> · <?= e($order['guest_email'] ?: '—') ?> · <?= e($order['guest_phone'] ?: '—') ?></p>
  <h2>Articles</h2>
  <ul><?php foreach ($items as $it): ?><li><?= e($it['product_name']) ?> × <?= (int)$it['quantity'] ?></li><?php endforeach; ?></ul>
  <form method="post" style="margin-top:1.5rem;max-width:420px">
    <?= csrf_field() ?>
    <label>Nouveau statut
      <select name="status">
        <?php foreach (['pending','awaiting_wire','awaiting_paypal','cod_confirmed','paid_manual','paid_stripe','shipped','cancelled'] as $s): ?>
        <option value="<?= $s ?>" <?= $order['status']===$s?'selected':'' ?>><?= e(order_status_label($s)) ?></option>
        <?php endforeach; ?>
      </select>
    </label>
    <label>Note<input name="note"></label>
    <button type="submit" class="xd-btn">Mettre à jour</button>
  </form>
  <h2>Historique</h2>
  <ul><?php foreach ($events as $ev): ?><li><?= e($ev['created_at']) ?> → <?= e($ev['to_status']) ?></li><?php endforeach; ?></ul>
</section>
<style>label{display:block;margin:1rem 0}input,select{width:100%;padding:.5rem;margin-top:.25rem}</style>
