CREATE MATERIALIZED VIEW IF NOT EXISTS people_in_space_mv TO people AS
SELECT
    tupleElement (line, 1) as craft,
    tupleElement (line, 2) as name,
    _inserted_at
FROM (
        SELECT arrayJoin (
                JSONExtract (
                    json_data, 'people', 'Array(Tuple(craft String, name String))'
                )
            ) as line, _inserted_at
        FROM people_in_space_raw
    );