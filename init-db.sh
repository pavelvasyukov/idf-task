#!/bin/bash
set -e

while ! clickhouse-client -u idftask --password idftask --query "SELECT 1" &> /dev/null; do
    sleep 1
done

echo "Executing $CLICKHOUSE_DB..."
for script in /init-sql-scripts/*.sql; do
    if [ -f "$script" ]; then
        echo "Executing $script..."
        clickhouse-client --database "$CLICKHOUSE_DB"  -u "$CLICKHOUSE_USER" --password "$CLICKHOUSE_PASSWORD" < "$script"
    fi
done 