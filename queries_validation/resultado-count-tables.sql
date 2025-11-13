/* VALIDATION: Conteo filas por tabla */
SELECT 'customers' AS tabla, COUNT(*) AS count FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items;
