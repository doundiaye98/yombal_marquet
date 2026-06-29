# -*- coding: utf-8 -*-
"""Generation de recus / factures PDF pour les commandes."""

import unicodedata
from html import escape

from models.constants import DELIVERY_COUNTRIES, ORDER_STATUS_LABELS
from models.order import Order

PAYMENT_METHOD_LABELS = {
    "stripe": "Carte bancaire (Stripe)",
    "paypal": "PayPal",
    "wire": "Virement bancaire",
    "cash_delivery": "Especes a la livraison",
    "demo": "Simulation (demo)",
}


def _pdf_safe(text: str) -> str:
    if not text:
        return ""
    text = text.replace("—", "-").replace("’", "'").replace("€", " EUR")
    return (
        unicodedata.normalize("NFKD", text)
        .encode("ascii", "ignore")
        .decode("ascii")
    )


def _euro(cents):
    return f"{(cents or 0) / 100:.2f} EUR"


def _country_label(code):
    return _pdf_safe(DELIVERY_COUNTRIES.get((code or "FR").upper(), code or "FR"))


def _payment_label(order: Order) -> str:
    if order.payment_method:
        return PAYMENT_METHOD_LABELS.get(order.payment_method, order.payment_method)
    return "En attente"


def invoice_html(order: Order, shop: dict | None = None) -> str:
    shop = shop or {}
    shop_name = _pdf_safe(shop.get("shop_name") or "Yombal Marche")
    shop_email = _pdf_safe(shop.get("shop_contact_email") or "")
    shop_phone = _pdf_safe(shop.get("shop_phone") or "")
    shop_addr = _pdf_safe(
        " · ".join(
            x
            for x in (shop.get("shop_address_line1"), shop.get("shop_address_line2"))
            if x
        )
    )

    doc_title = "Recu de commande" if order.is_paid() else "Confirmation de commande"
    status_label = _pdf_safe(ORDER_STATUS_LABELS.get(order.status, order.status))

    lines_html = ""
    for line in order.items:
        lines_html += (
            f"<tr>"
            f"<td>{escape(_pdf_safe(line.product_name))}</td>"
            f"<td align='right'>{line.quantity}</td>"
            f"<td align='right'>{_euro(line.unit_price_cents)}</td>"
            f"<td align='right'>{_euro(line.line_total_cents)}</td>"
            f"</tr>"
        )

    addr_parts = []
    if order.delivery_line1:
        addr_parts.append(_pdf_safe(order.delivery_line1))
    if order.delivery_line2:
        addr_parts.append(_pdf_safe(order.delivery_line2))
    city_line = " ".join(
        x for x in (order.delivery_postal_code, order.delivery_city) if x
    ).strip()
    if city_line:
        addr_parts.append(_pdf_safe(city_line))
    addr_block = "<br>".join(escape(p) for p in addr_parts) if addr_parts else "-"

    extra_rows = ""
    if order.promo_code:
        extra_rows += f"<br>Code promo : <strong>{escape(order.promo_code)}</strong>"
    if order.customer_notes:
        extra_rows += f"<br>Note client : {escape(_pdf_safe(order.customer_notes))}"
    if order.is_gift and order.gift_message:
        extra_rows += f"<br>Message cadeau : {escape(_pdf_safe(order.gift_message))}"

    return f"""
    <h1>{shop_name}</h1>
    <p>{shop_addr}<br>
    {f'E-mail : {shop_email}<br>' if shop_email else ''}
    {f'Tel. : {shop_phone}' if shop_phone else ''}</p>
    <hr>
    <h2>{doc_title}</h2>
    <p>
      <strong>Reference :</strong> {escape(order.public_ref)}<br>
      <strong>Date :</strong> {order.created_at.strftime('%d/%m/%Y a %H:%M')}<br>
      <strong>Statut :</strong> {status_label}<br>
      <strong>Mode de paiement :</strong> {escape(_pdf_safe(_payment_label(order)))}
    </p>
    <p>
      <strong>Client :</strong> {escape(_pdf_safe(order.customer_name()))}<br>
      <strong>E-mail :</strong> {escape(_pdf_safe(order.customer_email()))}<br>
      <strong>Telephone :</strong> {escape(_pdf_safe(order.customer_phone()))}
    </p>
    <p>
      <strong>Adresse de livraison :</strong><br>
      {addr_block}<br>
      <strong>Pays :</strong> {escape(_country_label(order.delivery_country))}
    </p>
    <h3>Detail des articles</h3>
    <table width="100%" border="1" cellspacing="0" cellpadding="6">
      <thead>
        <tr>
          <th align="left">Article</th>
          <th align="right">Qte</th>
          <th align="right">P.U. TTC</th>
          <th align="right">Total TTC</th>
        </tr>
      </thead>
      <tbody>{lines_html}</tbody>
    </table>
    <p align="right">
      Sous-total articles : {_euro(order.subtotal_cents)}<br>
      Frais de livraison : {_euro(order.shipping_cents)}<br>
      {"Reduction : - " + _euro(order.discount_cents) + "<br>" if order.discount_cents else ""}
      <strong>Total TTC : {_euro(order.total_cents)}</strong>
      {extra_rows}
    </p>
    <p><em>Merci pour votre confiance. Conservez ce document pour votre suivi.</em></p>
    """


def build_invoice_pdf(order: Order, shop: dict | None = None) -> bytes:
    try:
        from fpdf import FPDF
    except ImportError as exc:
        raise RuntimeError("fpdf2 requis : pip install fpdf2") from exc

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.write_html(invoice_html(order, shop))
    return bytes(pdf.output())
