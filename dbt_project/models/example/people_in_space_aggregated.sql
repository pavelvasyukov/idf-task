
{{ config(materialized='table') }}

SELECT 
    craft, 
    COUNT(name) AS astronaut_count 
FROM {{ source('idftask', 'people') }}
GROUP BY craft