SELECT *
FROM {{ ref('fact_fuel_prices') }}
WHERE effective_from > effective_to