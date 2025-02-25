
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
В volumes контейнера монтируются sql и bash скрипт для автоматического создания таблиц при поднятии контейнера
```bash
docker-compose up -d
```

Команды для создания таблиц вручную
```bash
cat scripts/01_create_raw_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
cat scripts/02_create_people_table.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
cat scripts/03_create_people_mv.sql | docker exec -i idf-task-clickhouse-1 clickhouse-client -u idftask --password idftask
```

### Запуск Python 

```powershell
.venv/Scripts/activate   
pip install -r requirements.txt
.venv/Scripts/python.exe main.py
```
#### Для unix/bash:
```bash
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Запуск Python тестов
```bash
pytest main_test.py -v 
```

### Запуск dbt модели и тестов 
из директории dbt_project 
```bash
dbt run --select people_in_space_aggregated
dbt test --select people_in_space_aggregateds
```
