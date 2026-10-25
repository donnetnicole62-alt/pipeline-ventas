
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select precio_unitario
from "warehouse"."main"."stg_ventas"
where precio_unitario is null



  
  
      
    ) dbt_internal_test