-- Capa staging: lee el CSV crudo y tipa las columnas.
select
    cast(fecha as date)             as fecha,
    cast(producto_id as integer)    as producto_id,
    cast(cantidad as integer)       as cantidad,
    cast(precio_unitario as double) as precio_unitario
from read_csv_auto('../data/ventas.csv', header = true)