-- Schéma de référence PostgreSQL — Yombal Marché
-- Les migrations officielles sont dans migrations/ (Alembic / Flask-Migrate).

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    name VARCHAR(100),
    phone VARCHAR(40),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS addresses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label VARCHAR(60) DEFAULT 'Domicile',
    line1 VARCHAR(200) NOT NULL,
    line2 VARCHAR(200),
    city VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country CHAR(2) NOT NULL DEFAULT 'FR',
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_addresses_user_id ON addresses(user_id);

CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(64) UNIQUE,
    slug VARCHAR(160) NOT NULL UNIQUE,
    name VARCHAR(220) NOT NULL,
    summary VARCHAR(600),
    description TEXT NOT NULL,
    price_cents INTEGER NOT NULL,
    category VARCHAR(80) NOT NULL,
    origin VARCHAR(160),
    weight_info VARCHAR(120),
    ingredients TEXT,
    allergens TEXT,
    usage_tips TEXT,
    conservation VARCHAR(300),
    stock_qty INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_products_category_active ON products(category, is_active);

CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    public_ref VARCHAR(32) NOT NULL UNIQUE,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    guest_email VARCHAR(120),
    guest_name VARCHAR(100),
    guest_phone VARCHAR(40),
    delivery_line1 VARCHAR(200),
    delivery_line2 VARCHAR(200),
    delivery_city VARCHAR(100),
    delivery_postal_code VARCHAR(20),
    delivery_country CHAR(2) DEFAULT 'FR',
    customer_notes TEXT,
    currency CHAR(3) NOT NULL DEFAULT 'EUR',
    subtotal_cents INTEGER NOT NULL DEFAULT 0,
    shipping_cents INTEGER NOT NULL DEFAULT 0,
    total_cents INTEGER NOT NULL,
    status VARCHAR(40) NOT NULL DEFAULT 'pending',
    payment_method VARCHAR(40),
    stripe_session_id VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_orders_status_created ON orders(status, created_at);
CREATE INDEX IF NOT EXISTS ix_orders_user_created ON orders(user_id, created_at);

CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    product_name VARCHAR(220) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price_cents INTEGER NOT NULL,
    line_total_cents INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_order_items_order_product ON order_items(order_id, product_id);

CREATE TABLE IF NOT EXISTS order_status_events (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    from_status VARCHAR(40),
    to_status VARCHAR(40) NOT NULL,
    note VARCHAR(500),
    actor_user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS ix_order_status_events_order_id ON order_status_events(order_id);
