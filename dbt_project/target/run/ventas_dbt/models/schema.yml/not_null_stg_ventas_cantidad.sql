
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select cantidad
from "warehouse"."main"."stg_ventas"
where cantidad is null



  
  
      
    ) dbt_internal_test