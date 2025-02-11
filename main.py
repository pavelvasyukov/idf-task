from os import getenv
from datetime import datetime
import time
import json
import logging
import requests
import clickhouse_connect


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = "http://api.open-notify.org/astros.json"

CLICKHOUSE_HOST = getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_USER = getenv("CLICKHOUSE_USER", "idftask")
CLICKHOUSE_PASSWORD = getenv("CLICKHOUSE_PASSWORD", "idftask")
CLICKHOUSE_DATABASE = getenv("CLICKHOUSE_DATABASE", "idftask")


def fetch_data(url, max_retries=5):
    """Function that performs an HTTP request with error handling and retries."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                try:
                    return json.dumps(response.json())
                except json.JSONDecodeError as e:
                    logging.error("JSON parsing error: %s", e)
                    return None

            elif response.status_code in (302, 429):
                wait_time = max(int(response.headers.get("Retry-After"),2**attempt))
                logging.warning(
                    "Received %s, retrying in %s sec.", response.status_code, wait_time
                )
                time.sleep(wait_time)

            elif 400 <= response.status_code < 500:
                logging.error(
                    "Client error: %s - %s", response.status_code, response.text
                )
                return None

            elif 500 <= response.status_code < 600:
                logging.error(
                    "Server error: %s - %s", response.status_code, response.text
                )
                time.sleep(2**attempt)

            else:
                logging.error("Unexpected HTTP status code: %s", response.status_code)
                return None

        except requests.exceptions.RequestException as e:
            logging.error("Request error (attempt %s): %s", attempt + 1, e)

    logging.error("All attempts failed")
    return None


def save_to_clickhouse(data):
    if not data:
        logging.error("No data to insert into ClickHouse")
        return

    try:
        with clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            user=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DATABASE,
        ) as client:
            client.command(
                """
                CREATE TABLE IF NOT EXISTS RAW_TABLE (
                    json_data String,
                    _inserted_at DateTime DEFAULT now()
                ) ENGINE = MergeTree()
                ORDER BY _inserted_at;
                """
            )
            client.insert("RAW_TABLE", [(data, datetime.now())])
            client.command("OPTIMIZE TABLE RAW_TABLE DEDUPLICATE;")
            logging.info("Data successfully inserted into ClickHouse")
    except Exception as e:
        logging.error("Error while working with ClickHouse: %s", e)


def main():
    logging.info("Starting script")

    data = fetch_data(URL)
    if data:
        logging.info("Data successfully retrieved")
        save_to_clickhouse(data)
    else:
        logging.error("Data was not retrieved")


if __name__ == "__main__":
    main()
