/* VALIDATION: Comparar suma total almacenada en orders vs suma calculada desde order_items */
SELECT
  (SELECT SUM(total) FROM orders)::numeric(18,2) AS sum_total_col,
  (SELECT SUM(qty * unit_price) FROM order_items)::numeric(18,2) AS sum_calc;
