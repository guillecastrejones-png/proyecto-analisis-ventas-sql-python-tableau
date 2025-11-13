-- 02_compare_sum_order_items.sql
-- Comparar suma total almacenada en order_items.total vs suma calculada (qty * unit_price)
SELECT
  SUM(total)::numeric(18,2) AS sum_total_col,
  SUM(qty * unit_price)::numeric(18,2) AS sum_calc,
  (SUM(total) - SUM(qty * unit_price))::numeric(18,2) AS diff
FROM order_items;
