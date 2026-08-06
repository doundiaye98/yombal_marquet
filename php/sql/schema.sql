-- Yombal Market — schéma MySQL (Hostinger)
-- Charset: utf8mb4
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE IF NOT EXISTS users (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(120) NOT NULL,
  password_hash VARCHAR(256) NOT NULL,
  name VARCHAR(100) NULL,
  phone VARCHAR(40) NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_users_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS addresses (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id INT UNSIGNED NOT NULL,
  label VARCHAR(60) DEFAULT 'Domicile',
  line1 VARCHAR(200) NOT NULL,
  line2 VARCHAR(200) NULL,
  city VARCHAR(100) NOT NULL,
  postal_code VARCHAR(20) NOT NULL,
  country CHAR(2) NOT NULL DEFAULT 'FR',
  is_default TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY ix_addresses_user (user_id),
  CONSTRAINT fk_addresses_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS producers (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug VARCHAR(160) NOT NULL,
  name VARCHAR(200) NOT NULL,
  region VARCHAR(160) NULL,
  flagship_product VARCHAR(200) NULL,
  experience VARCHAR(120) NULL,
  method VARCHAR(200) NULL,
  monthly_production VARCHAR(120) NULL,
  story TEXT NULL,
  avatar_emoji VARCHAR(16) NULL,
  audio_url VARCHAR(255) NULL,
  map_x DECIMAL(8,2) NULL,
  map_y DECIMAL(8,2) NULL,
  map_label VARCHAR(120) NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_producers_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS products (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  sku VARCHAR(64) NULL,
  slug VARCHAR(160) NOT NULL,
  name VARCHAR(220) NOT NULL,
  summary VARCHAR(600) NULL,
  description TEXT NOT NULL,
  price_cents INT NOT NULL,
  category VARCHAR(80) NOT NULL,
  origin VARCHAR(160) NULL,
  weight_info VARCHAR(120) NULL,
  ingredients TEXT NULL,
  allergens TEXT NULL,
  usage_tips TEXT NULL,
  conservation VARCHAR(300) NULL,
  stock_qty INT NULL,
  image VARCHAR(255) NULL,
  icon VARCHAR(8) NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  producer_id INT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_products_slug (slug),
  UNIQUE KEY uq_products_sku (sku),
  KEY ix_products_category_active (category, is_active),
  KEY ix_products_producer (producer_id),
  CONSTRAINT fk_products_producer FOREIGN KEY (producer_id) REFERENCES producers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS product_images (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  product_id INT UNSIGNED NOT NULL,
  image VARCHAR(255) NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  KEY ix_product_images_product (product_id),
  CONSTRAINT fk_product_images_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS orders (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  public_ref VARCHAR(32) NOT NULL,
  user_id INT UNSIGNED NULL,
  guest_email VARCHAR(120) NULL,
  guest_name VARCHAR(100) NULL,
  guest_phone VARCHAR(40) NULL,
  delivery_line1 VARCHAR(200) NULL,
  delivery_line2 VARCHAR(200) NULL,
  delivery_city VARCHAR(100) NULL,
  delivery_postal_code VARCHAR(20) NULL,
  delivery_country CHAR(2) NOT NULL DEFAULT 'FR',
  customer_notes TEXT NULL,
  gift_message TEXT NULL,
  is_gift TINYINT(1) NOT NULL DEFAULT 0,
  promo_code VARCHAR(40) NULL,
  discount_cents INT NOT NULL DEFAULT 0,
  notify_status_updates TINYINT(1) NOT NULL DEFAULT 1,
  currency CHAR(3) NOT NULL DEFAULT 'EUR',
  subtotal_cents INT NOT NULL DEFAULT 0,
  shipping_cents INT NOT NULL DEFAULT 0,
  total_cents INT NOT NULL,
  status VARCHAR(40) NOT NULL DEFAULT 'pending',
  payment_method VARCHAR(40) NULL,
  stripe_session_id VARCHAR(255) NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uq_orders_public_ref (public_ref),
  KEY ix_orders_status_created (status, created_at),
  KEY ix_orders_user_created (user_id, created_at),
  KEY ix_orders_guest_email (guest_email),
  KEY ix_orders_stripe (stripe_session_id),
  CONSTRAINT fk_orders_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS order_items (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  order_id INT UNSIGNED NOT NULL,
  product_id INT UNSIGNED NOT NULL,
  product_name VARCHAR(220) NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  unit_price_cents INT NOT NULL,
  line_total_cents INT NOT NULL,
  bundle_type VARCHAR(20) NULL,
  bundle_slug VARCHAR(120) NULL,
  KEY ix_order_items_order_product (order_id, product_id),
  CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS order_status_events (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  order_id INT UNSIGNED NOT NULL,
  from_status VARCHAR(40) NULL,
  to_status VARCHAR(40) NOT NULL,
  note VARCHAR(500) NULL,
  actor_user_id INT UNSIGNED NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY ix_ose_order (order_id),
  KEY ix_ose_created (created_at),
  CONSTRAINT fk_ose_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
  CONSTRAINT fk_ose_actor FOREIGN KEY (actor_user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS contact_messages (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(120) NOT NULL,
  subject VARCHAR(200) NOT NULL,
  message TEXT NOT NULL,
  is_read TINYINT(1) NOT NULL DEFAULT 0,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS faq_items (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  question VARCHAR(400) NOT NULL,
  answer TEXT NOT NULL,
  sort_order INT NOT NULL DEFAULT 0,
  is_active TINYINT(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS delivery_zones (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  postal_prefix VARCHAR(20) NULL,
  price_cents INT NOT NULL DEFAULT 0,
  free_over_cents INT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  sort_order INT NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS promo_codes (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  code VARCHAR(40) NOT NULL,
  discount_percent INT NULL,
  discount_cents INT NULL,
  min_order_cents INT NULL,
  max_uses INT NULL,
  used_count INT NOT NULL DEFAULT 0,
  valid_until DATETIME NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_promo_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS site_settings (
  `key` VARCHAR(80) PRIMARY KEY,
  `value` TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS recipes (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug VARCHAR(160) NOT NULL,
  title VARCHAR(220) NOT NULL,
  summary VARCHAR(600) NULL,
  type VARCHAR(60) NULL,
  image VARCHAR(255) NULL,
  steps_json TEXT NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_recipes_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS recipe_lines (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  recipe_id INT UNSIGNED NOT NULL,
  product_id INT UNSIGNED NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  note VARCHAR(200) NULL,
  CONSTRAINT fk_rl_recipe FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE,
  CONSTRAINT fk_rl_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS coffrets (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  slug VARCHAR(160) NOT NULL,
  title VARCHAR(220) NOT NULL,
  theme VARCHAR(80) NULL,
  summary VARCHAR(600) NULL,
  image VARCHAR(255) NULL,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  UNIQUE KEY uq_coffrets_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS coffret_lines (
  id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  coffret_id INT UNSIGNED NOT NULL,
  product_id INT UNSIGNED NOT NULL,
  quantity INT NOT NULL DEFAULT 1,
  CONSTRAINT fk_cl_coffret FOREIGN KEY (coffret_id) REFERENCES coffrets(id) ON DELETE CASCADE,
  CONSTRAINT fk_cl_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

SET FOREIGN_KEY_CHECKS = 1;

-- Paramètres par défaut
INSERT INTO site_settings (`key`, `value`) VALUES
  ('shop_name', 'Yombal Market'),
  ('contact_email', 'compta@universdiasporas.com')
ON DUPLICATE KEY UPDATE `value` = VALUES(`value`);

-- Zone livraison France par défaut
INSERT INTO delivery_zones (name, postal_prefix, price_cents, free_over_cents, is_active, sort_order)
SELECT 'France métropolitaine', NULL, 590, 6000, 1, 1
FROM DUAL
WHERE NOT EXISTS (SELECT 1 FROM delivery_zones LIMIT 1);
