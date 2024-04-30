import os
import psycopg2
from prometheus_client import start_http_server, Gauge
import time

# Define Prometheus metrics
metrics = {}

def get_env_vars_ending_with(suffix):
    env_vars = {}
    for key, value in os.environ.items():
        if key.endswith(suffix):
            env_vars[key] = value
    return env_vars

def create_query_alerts():
    queries = get_env_vars_ending_with("_ALERT_QUERY")
    query_alerts = []

    print("Monitored queries:")

    for query in queries:
        query_name = query
        query = os.environ.get(query_name)
        query_db = os.environ.get(f'{query_name}_DATABASE')

        print(query_name, query, query_db)

        query_alerts.append({"name": query_name, "query": query, "database": query_db})

    return query_alerts

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

    queries = create_query_alerts()
    # [{'name': 'EXAMPLE_QUERY_ALERT_QUERY', 'query': 'SELECT COUNT(*) FROM SOME_TABLE;', 'database': 'some_database'}, {'name': 'EXAMPLE_QUERY_2_ALERT_QUERY', 'query': 'SELECT COUNT(*) FROM OTHER_TABLE;', 'database': 'other_database'}]

    # queries = {
    #     "example-query": os.environ.get('EXAMPLE_QUERY'),
    #     "example-query-2": os.environ.get('EXAMPLE_QUERY_2')
    # }


    # Create Prometheus metrics for each query
    for query in queries:
        query_name = query.get('name')
        metrics[query_name] = Gauge(query_name, f'Result of {query_name}')

    while True:
        # Execute each query and update Prometheus metric
        for query in queries:
            connection_string = f"dbname='{query.get('database')}' user='{db_user}' host='{db_host}' port='{db_port}' password='{db_password}'"
            result = execute_query(connection_string, query.get('query'))
            print(str(connection_string))
            print(str(result))
            if result is not None:
                metrics[query_name].set(result)

        # Sleep for some time before executing the queries again
        time.sleep(60)  # Example: Query every minute