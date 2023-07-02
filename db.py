import argparse
import sqlite3

# check: https://www.sqlitetutorial.net/sqlite-python/

sql_create_notebooks_table = """
CREATE TABLE IF NOT EXISTS notebooks (
    id integer PRIMARY KEY,
    url text,
    location text,
); """

sql_insert_notebook = """
INSERT INTO notebooks(url, saved_as)
VALUES(?,?) """

sql_get_notebooks = """
SELECT * FROM notebooks """

sql_update_nb_location = """
UPDATE tasks
    SET location = ?
WHERE location = ?  """

sql_clear_notebooks_table =  """
DELETE FROM notebooks """


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def open_conn(action):
    conn = None
    try:
        conn = sqlite3.connect("./notebooks/notebooks.db")
        action(conn)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def execute_sql(conn, sql, *args):
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()


def execute_sql_with_action(conn, sql, action, *args):
    cur = conn.cursor()
    cur.execute(sql, args)
    conn.commit()
    action(cur)


def insert_notebooks(notebooks):
    def action(conn):
        create_table(conn, sql_create_notebooks_table)
        for notebook in notebooks:
            execute_sql(conn, sql_insert_notebook, notebook)
    open_conn(action)


def update_notebook_location(old_location, new_location):
    open_conn(lambda conn: execute_sql(conn, sql_update_nb_location, (new_location, old_location)))


def get_notebooks():
    fetch_all = lambda cur: cur.fetchall()
    open_conn(lambda conn: execute_sql_with_action(conn, sql_get_notebooks, fetch_all))


def clear_notebooks()
    open_conn(lambda conn: execute_sql(conn, sql_clear_notebooks_table))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-action')
    parser.add_argument('--old-location')
    parser.add_argument('--new-location')
    args = parser.parse_args()
    if args.action == 'update_location':
        update_notebook_location(args.new_location, args.old_location)
