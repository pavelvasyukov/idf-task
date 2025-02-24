CREATE TABLE IF NOT EXISTS people (
    craft String,
    name String,
    _inserted_at DateTime
) ENGINE = ReplacingMergeTree (_inserted_at)
ORDER BY (name, craft);