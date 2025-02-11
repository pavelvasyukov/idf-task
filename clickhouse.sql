-- Active: 1739131021858@@127.0.0.1@8123@idftask



OPTIMIZE TABLE RAW_TABLE DEDUPLICATE;


CREATE IF NOT EXISTS TABLE PARSED_TABLE (
    craft String,
    name String,
    _inserted_at DateTime
) ENGINE = MergeTree(_inserted_at)
ORDER BY (name,craft);


CREATE MATERIALIZED VIEW MV TO PARSED_TABLE AS
SELECT
    JSONExtractString(data, 'craft') AS craft,
    JSONExtractString(data, 'name') AS name,
    _inserted_at
FROM RAW_TABLE;