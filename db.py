import argparse
import sqlite3

# check: https://www.sqlitetutorial.net/sqlite-python/

sql_create_notebooks_table = """
CREATE TABLE IF NOT EXISTS notebooks (
    id integer PRIMARY KEY,
    url text,
    location text,
    filesize text,
    analysis_status text,
    analysis_time real,
    pre_processing_leakages integer,
    overlap_leakages integer,
    no_independence_test_data integer
); """

sql_insert_notebook = """
INSERT INTO notebooks(url, location)
VALUES(?,?) """

sql_get_notebooks = """
SELECT * FROM notebooks """

sql_get_valid_notebooks = """
SELECT * FROM notebooks WHERE location LIKE "%/valid/%" ORDER BY location desc"""

sql_update_nb_location = """
UPDATE notebooks
    SET location = ?
WHERE location = ? """

sql_clear_notebooks_table =  """
DROP TABLE IF EXISTS notebooks; """

sql_update_nb_analysis_data = """
UPDATE notebooks
    SET filesize = ?,
    analysis_status = ?,
    analysis_time = ?,
    pre_processing_leakages = ?,
    overlap_leakages = ?,
    no_independence_test_data = ?
WHERE id = ? """


def open_conn(action):
    conn = None
    try:
        conn = sqlite3.connect("./notebooks/notebooks.db")
        result = action(conn)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return result

def execute_sql(conn, sql, *args):
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()


def execute_sql_with_action(conn, sql, action, *args):
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    return action(cur)


def insert_notebooks(notebooks):
    def action(conn):
        execute_sql(conn, sql_create_notebooks_table)
        for notebook in notebooks:
            url = notebook[0]
            location = notebook[1]
            execute_sql(conn, sql_insert_notebook, url, location)
    open_conn(action)


def update_notebook_location(old_location, new_location):
    open_conn(lambda conn: execute_sql(conn, sql_update_nb_location, new_location, old_location))


def get_notebooks():
    fetch_all = lambda cur: cur.fetchall()
    return open_conn(lambda conn: execute_sql_with_action(conn, sql_get_notebooks, fetch_all))


def clear_notebooks():
    open_conn(lambda conn: execute_sql(conn, sql_clear_notebooks_table))


def get_valid_notebooks():
    fetch_all = lambda cur: cur.fetchall()
    return open_conn(lambda conn: execute_sql_with_action(conn, sql_get_valid_notebooks, fetch_all))


def update_nb_analysis_data(nb_id, nb_size, a_status, a_time, *leakages):
    return open_conn(lambda conn: execute_sql(conn, sql_update_nb_analysis_data, nb_size, a_status, a_time, *leakages, nb_id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-action')
    parser.add_argument('--old-location')
    parser.add_argument('--new-location')
    args = parser.parse_args()
    if args.action == 'update_location':
        update_notebook_location(args.old_location, args.new_location)
