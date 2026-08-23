WITH source_data AS (
    SELECT
        effective_from,
        effective_to,
        town,
        super_pms,
        diesel_ago,
        kerosene_ik,
        source_url,
        extracted_at,
        loaded_at
    FROM `epra-fuel-data-platform.epra_raw.epra_fuel_prices`
),
cleaned AS (
    SELECT
        CAST(effective_from AS DATE) AS effective_from,
        CAST(effective_to AS DATE) AS effective_to,
        TRIM(town) AS town,
        CAST(super_pms AS NUMERIC) AS super_pms,
        CAST(diesel_ago AS NUMERIC) AS diesel_ago,
        CAST(kerosene_ik AS NUMERIC) AS kerosene_ik,
        source_url,
        extracted_at,
        loaded_at
    FROM source_data
)
SELECT * FROM cleaned