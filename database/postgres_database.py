import psycopg2
from psycopg2 import sql


class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database.")
        except psycopg2.Error as e:
            print(f"Unable to connect to the database. Error: {e}")

    def is_connected(self):
        return self.connection is not None

    def reconnect(self):
        if not self.is_connected():
            self.connect()

    def close(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query, params=None):
        self.reconnect()
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()

    def insert_data(self, table, data):
        columns = data.keys()
        values = [data[col] for col in columns]
        query = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(table),
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        self.execute_query(query, tuple(values))

    def update_data(self, table, data, condition):
        set_clause = sql.SQL(', ').join(
            sql.SQL("{} = {}").format(sql.Identifier(col), sql.Placeholder())
            for col in data.keys()
        )
        query = sql.SQL("UPDATE {} SET {} WHERE {}").format(
            sql.Identifier(table),
            set_clause,
            sql.SQL(condition)
        )
        self.execute_query(query, tuple(data.values()))

    def select_data(self, table, columns="*", condition=None):
        query = sql.SQL("SELECT {} FROM {}").format(
            sql.SQL(columns),
            sql.Identifier(table)
        )
        if condition:
            query += sql.SQL(" WHERE {}").format(sql.SQL(condition))
        self.reconnect()
        try:
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return rows
        except psycopg2.Error as e:
            print(f"Error executing SELECT query: {e}")
            return []
