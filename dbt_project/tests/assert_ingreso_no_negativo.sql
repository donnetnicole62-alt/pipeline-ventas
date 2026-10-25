select * from {{ ref('fct_ingresos_diarios') }} where ingreso_total < 0
