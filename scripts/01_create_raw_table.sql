CREATE TABLE IF NOT EXISTS people_in_space_raw (
    json_data String,
    _inserted_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree (_inserted_at)
ORDER BY json_data;