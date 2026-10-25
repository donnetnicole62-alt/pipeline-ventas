
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ingreso_total
from "warehouse"."main"."fct_ingresos_diarios"
where ingreso_total is null



  
  
      
    ) dbt_internal_test