#!/bin/bash


docker-compose up -d


# cat scripts/01_create_raw_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
# cat scripts/02_create_people_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
# cat scripts/03_create_people_mv.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask


source .venv/bin/activate
pip install -r requirements.txt

python main.py

pytest main_test.py -v

dbt run --select people_in_space_aggregated
dbt test --select people_in_space_aggregated