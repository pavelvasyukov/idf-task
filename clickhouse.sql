-- Active: 1739131021858@@127.0.0.1@8123@idftask

CREATE TABLE IF NOT EXISTS people_in_space_raw (
    json_data String,
    _inserted_at DateTime DEFAULT now()
) ENGINE = ReplacingMergeTree (_inserted_at)
ORDER BY json_data;


CREATE TABLE IF NOT EXISTS people_in_space (
    craft String,
    name String,
    _inserted_at DateTime
) ENGINE = MergeTree ()
ORDER BY (name, craft);


CREATE MATERIALIZED VIEW IF NOT EXISTS people_in_space_mv TO people_in_space AS
SELECT
    tupleElement(line, 1) as craft,
    tupleElement(line, 2) as name,
    _inserted_at 
FROM (
        SELECT arrayJoin (
                JSONExtract (
                    json_data, 'people', 'Array(Tuple(craft String, name String))'
                )
            ) as line, _inserted_at
        FROM people_in_space_raw
    );


SELECT * FROM people_in_space;

SELECT * FROM people_in_space_aggregated;