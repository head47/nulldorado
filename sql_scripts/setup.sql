CREATE DATABASE nulldorado_data;

-- nulldorado_data.shop_category definition

CREATE TABLE nulldorado_data.shop_category (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `picture` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- nulldorado_data.shop_order definition

CREATE TABLE nulldorado_data.shop_order (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone` varchar(16) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `items` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`items`)),
  `order_status` varchar(1) COLLATE utf8mb4_unicode_ci NOT NULL,
  `address` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- nulldorado_data.shop_subcategory definition

CREATE TABLE nulldorado_data.shop_subcategory (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parent_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `shop_subcategory_parent_id_36cd4c95_fk_shop_category_id` (`parent_id`),
  CONSTRAINT `shop_subcategory_parent_id_36cd4c95_fk_shop_category_id` FOREIGN KEY (`parent_id`) REFERENCES `shop_category` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- nulldorado_data.shop_item definition

CREATE TABLE nulldorado_data.shop_item (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `picture` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(12,2) NOT NULL,
  `parent_id` int(11) NOT NULL,
  `new` tinyint(1) NOT NULL,
  `available` int(10) unsigned NOT NULL CHECK (`available` >= 0),
  PRIMARY KEY (`id`),
  KEY `shop_item_parent_id_f0ab547a_fk_shop_subcategory_id` (`parent_id`),
  CONSTRAINT `shop_item_parent_id_f0ab547a_fk_shop_subcategory_id` FOREIGN KEY (`parent_id`) REFERENCES `shop_subcategory` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- privileges

CREATE USER djangouser@'10.0.2.2' IDENTIFIED BY 'verysecurepassword';
GRANT ALL ON nulldorado_data.* TO djangouser@'10.0.2.2';
FLUSH PRIVILEGES;
EXIT;
