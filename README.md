
### 1) Поднять в докере Clickhouse (актуальную версию)
    
### 2) На Python написать функциональность по скачиванию и заливке данных в Clickhouse в сыром виде (JSON) 
http://api.open-notify.org/astros.json  

- Обработать возможные ошибки (429 статус и прочее), в случае получения ждать, после 5 попыток(то есть все были неудачными) выбрасывать ошибку  
- Ретрай таймаут должен быть нарастающий  
- На Clickhouse должны быть ТОЛЬКО вставки, без DML операций, дедупликацию делать силами Clickhouse (replacing движок таблицы + OPTIMIZE ...)  

### 3) В Clickhouse реализовать парсинг сырых данных с помощью materialized view (на выходе должна быть таблица people с колонками craft, name, _inseserted_at)
 Полный флоу RAW_TABLE (сюда вставляет данные функция из п.2) -> MV -> PARSED_TABLE

###  4) Поставить DBT\DBT-clickhouse, создать проект, в проекте создать модель с логикой на свое усмотрение



# Информация для запуска проекта:


### Запуск docker compose и команды для создания таблиц
```
docker-compose up -d
cat create_raw_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
cat create_people_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
cat create_people_mv.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
```

### Запуск Python 
```
.venv/Scripts/activate   
pip install -r requirements.txt
.venv/Scripts/python.exe c:/projects/idf-task/main.py
```

### Запуск Python тестов
```
pytest main_test.py -v 
```

### Запуск dbt модели и тестов
```
dbt run --select people_in_space_aggregated
dbt test --select people_in_space_aggregateds
```
