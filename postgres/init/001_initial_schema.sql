CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.epra_fuel_prices (
    effective_from DATE NOT NULL,
    effective_to DATE NOT NULL,
    town TEXT NOT NULL,
    super_pms NUMERIC(10, 2) NOT NULL,
    diesel_ago NUMERIC(10, 2) NOT NULL,
    kerosene_ik NUMERIC(10, 2) NOT NULL,
    source_url TEXT NOT NULL,
    extracted_at TIMESTAMPTZ NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (effective_from, effective_to, town),
    CHECK (effective_to >= effective_from),
    CHECK (super_pms >= 0 AND diesel_ago >= 0 AND kerosene_ik >= 0)
);

CREATE SCHEMA IF NOT EXISTS audit;

CREATE TABLE IF NOT EXISTS audit.pipeline_runs (
    run_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    airflow_run_id TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    completed_at TIMESTAMPTZ,
    status TEXT NOT NULL CHECK (status IN ('RUNNING', 'SUCCESS', 'FAILED')),
    rows_extracted BIGINT NOT NULL DEFAULT 0 CHECK (rows_extracted >= 0),
    rows_transformed BIGINT NOT NULL DEFAULT 0 CHECK (rows_transformed >= 0),
    rows_loaded BIGINT NOT NULL DEFAULT 0 CHECK (rows_loaded >= 0),
    error_message TEXT,
    CHECK (
        (status = 'RUNNING' AND completed_at IS NULL)
        OR (status IN ('SUCCESS', 'FAILED') AND completed_at IS NOT NULL)
    )
);

ALTER TABLE audit.pipeline_runs
    ADD COLUMN IF NOT EXISTS airflow_run_id TEXT;

UPDATE audit.pipeline_runs
SET airflow_run_id = 'legacy-' || run_id::TEXT
WHERE airflow_run_id IS NULL;

ALTER TABLE audit.pipeline_runs
    ALTER COLUMN airflow_run_id SET NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_pipeline_runs_airflow_run_id
    ON audit.pipeline_runs (airflow_run_id);