import os
import psycopg2
from prometheus_client import start_http_server, Gauge
import time

# Define Prometheus metrics
metrics = {}

def execute_query(connection_string, query):
    try:
        conn = psycopg2.connect(connection_string)
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchone()[0]  # Assuming a single value is returned

        cur.close()
        conn.close()

        return result

    except psycopg2.Error as e:
        print("Error executing query:", e)
        return None

if __name__ == '__main__':
    # Start HTTP server to expose Prometheus metrics
    start_http_server(8000)

    db_host = os.environ.get('POSTGRES_IP')
    db_port = os.environ.get('POSTGRES_PORT') or '5432'
    db_user = os.environ.get('POSTGRES_USER')
    db_password = os.environ.get('POSTGRES_PASSWORD')

    # Construct connection string
    connection_string = f"dbname='postgres' user='{db_user}' host='{db_host}' port='{db_port}' password='{db_password}'"

    # Read queries from environment variables
    queries = {
        "example-query": os.environ.get('EXAMPLE_QUERY'),
        "example-query-2": os.environ.get('EXAMPLE_QUERY_2')
    }

    # Create Prometheus metrics for each query
    for query_name, _ in queries.items():
        metrics[query_name] = Gauge(query_name, f'Result of {query_name}')

    while True:
        # Execute each query and update Prometheus metric
        for query_name, query in queries.items():
            result = execute_query(connection_string, query)
            if result is not None:
                metrics[query_name].set(result)

        # Sleep for some time before executing the queries again
        time.sleep(60)  # Example: Query every minute