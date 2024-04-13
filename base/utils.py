import psycopg2


def create_test_results_table(cursor):
    create_table_query = '''CREATE TABLE IF NOT EXISTS test_results
                            (id SERIAL PRIMARY KEY,
                            session_id VARCHAR(255) NOT NULL,
                            start_time TIMESTAMP,
                            test_name VARCHAR(255) NOT NULL,
                            result VARCHAR(50) NOT NULL,
                            duration FLOAT,
                            status VARCHAR(50));'''
    cursor.execute(create_table_query)


def insert_test_result_to_postgres(conn_cred, session_id, test_name, result, duration, start_time, status):
    connection = None
    try:
        connection = psycopg2.connect(**conn_cred)
        cursor = connection.cursor()

        create_test_results_table(cursor)

        postgres_insert_query = """ INSERT INTO test_results (session_id, test_name, result, duration, start_time, status) 
                                    VALUES (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (session_id, test_name, result, duration, start_time, status)
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        if connection:  # noqa
            cursor.close()  # noqa
            connection.close()  # noqa
