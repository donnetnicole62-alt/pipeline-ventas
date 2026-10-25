-- Test singular: falla si devuelve filas.
select * from {{ ref('stg_ventas') }} where cantidad <= 0
