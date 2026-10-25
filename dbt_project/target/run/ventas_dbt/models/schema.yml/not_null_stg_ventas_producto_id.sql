
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select producto_id
from "warehouse"."main"."stg_ventas"
where producto_id is null



  
  
      
    ) dbt_internal_test