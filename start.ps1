
docker-compose up -d
cat create_raw_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
cat create_people_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
cat create_people_mv.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask



.venv/Scripts/activate   
pip install -r requirements.txt
.venv/Scripts/python.exe c:/projects/idf-task/main.py

pytest main_test.py -v 

dbt run --select people_in_space_aggregated
dbt test --select people_in_space_aggregateds