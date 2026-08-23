WITH locations AS (
    SELECT DISTINCT
        town
    FROM {{ ref('stg_epra_fuel_prices') }}
    WHERE town IS NOT NULL
)
SELECT
    ROW_NUMBER() OVER (ORDER BY town) AS location_key,
    town
FROM locations