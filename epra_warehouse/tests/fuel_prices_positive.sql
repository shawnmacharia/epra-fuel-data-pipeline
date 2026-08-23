SELECT *
FROM {{ ref('fact_fuel_prices') }}
WHERE price <= 0