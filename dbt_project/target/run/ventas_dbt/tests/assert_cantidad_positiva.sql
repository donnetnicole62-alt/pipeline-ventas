
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  -- Test singular: falla si devuelve filas.
select * from "warehouse"."main"."stg_ventas" where cantidad <= 0
  
  
      
    ) dbt_internal_test