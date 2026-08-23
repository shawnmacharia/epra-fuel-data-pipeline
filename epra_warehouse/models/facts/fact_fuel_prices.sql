WITH source AS (
    SELECT * FROM {{ ref('stg_epra_fuel_prices') }}
),
location AS (
    SELECT location_key, town FROM {{ ref('dim_location') }}
),
unpivoted AS (
    SELECT effective_from, effective_to, town, 'PMS' AS fuel_code, super_pms AS price, source_url, extracted_at, loaded_at FROM source
    UNION ALL
    SELECT effective_from, effective_to, town, 'AGO' AS fuel_code, diesel_ago AS price, source_url, extracted_at, loaded_at FROM source
    UNION ALL
    SELECT effective_from, effective_to, town, 'IK' AS fuel_code, kerosene_ik AS price, source_url, extracted_at, loaded_at FROM source
),
final AS (
    SELECT
        CAST(FORMAT_DATE('%Y%m%d', u.effective_from) AS INT64) AS date_key,
        l.location_key,
        CASE u.fuel_code WHEN 'PMS' THEN 1 WHEN 'AGO' THEN 2 WHEN 'IK' THEN 3 END AS fuel_key,
        u.effective_from,
        u.effective_to,
        u.price,
        u.source_url,
        u.extracted_at,
        u.loaded_at
    FROM unpivoted u
    INNER JOIN location l ON u.town = l.town
)
SELECT * FROM final