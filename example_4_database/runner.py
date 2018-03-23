import requests
import sqlite3
from io import StringIO


def save_db(data_dump):
    temp_file = StringIO()
    temp_file.writelines(data_dump)
    temp_file.seek(0)

    files = {'scans': temp_file}
    values = {'DB': 'scans', 'OUT': 'db', 'SHORT': 'short'}
    requests.post('http://127.0.0.1:5002/save_db_once', files=files, data=values)


def load_db():
    r = requests.get('http://127.0.0.1:5002/load_db')
    with sqlite3.connect(':memory:') as conn:
        cursor = conn.cursor()
        s = StringIO(r.content.decode())
        sql = s.read()
        conn.executescript(sql)

        try:
            print(cursor.execute('SELECT * FROM scan_data').fetchall())
        except sqlite3.OperationalError as e:
            print('This will not be hit because table exists.')
            print(e)


def main():
    with sqlite3.connect(':memory:') as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE scan_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            hostname TEXT,
            ip TEXT
        );""")

        for host in [{'hostname': 'computer1', 'ip': '127.0.0.1'}, {'hostname': 'computer2', 'ip': '169.255.255.255'}]:
            query = """
            INSERT INTO scan_data (hostname, ip)
            VALUES (:hostname, :ip)"""
            cursor.execute(query, host)

        print(cursor.execute('SELECT * FROM scan_data').fetchall())

        save_db(conn.iterdump())

    with sqlite3.connect(':memory:') as conn:
        cursor = conn.cursor()
        try:
            print(cursor.execute('SELECT * FROM scan_data').fetchall())
        except sqlite3.OperationalError as e:
            print('This will be hit.')
            print(e)

    load_db()


if __name__ == '__main__':
    main()
