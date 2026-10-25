
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  select * from "warehouse"."main"."fct_ingresos_diarios" where ingreso_total < 0
  
  
      
    ) dbt_internal_test