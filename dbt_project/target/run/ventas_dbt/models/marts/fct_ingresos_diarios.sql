
    

    create  table
      "warehouse"."main"."fct_ingresos_diarios__dbt_tmp"
  
    
    as (
      -- Capa mart: mismo resultado que el job PySpark, expresado en SQL (permite cruzar resultados).
select
    fecha,
    producto_id,
    round(sum(cantidad * precio_unitario), 2) as ingreso_total
from "warehouse"."main"."stg_ventas"
group by fecha, producto_id
order by fecha, producto_id
    );
    
  