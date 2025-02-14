
{{ config(materialized='table') }}

SELECT 
    craft, 
    COUNT(name) AS astronaut_count 
FROM {{ source('idftask', 'people_in_space') }}
GROUP BY craft