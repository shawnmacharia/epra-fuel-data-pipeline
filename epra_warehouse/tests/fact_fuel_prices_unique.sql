SELECT
    effective_from,
    effective_to,
    location_key,
    fuel_key,
    COUNT(*) AS duplicate_count
FROM {{ ref('fact_fuel_prices') }}
GROUP BY
    effective_from,
    effective_to,
    location_key,
    fuel_key
HAVING COUNT(*) > 1