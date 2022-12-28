import random
from contextlib import closing

import mysql.connector
from mysql.connector import OperationalError

from config.database import DbCredentials


def create_mysql_connection(credential, attempt=1):
    try:
        return mysql.connector.connect(
            host=credential['host'],
            user=credential['user'],
            password=credential['password'],
            database=credential['database'],
            autocommit=True
        )
    except Exception as e:
        # add error log and print traceback
        error_str = f'MySQL connection to {credential["database"]} failed. (Host: {credential["host"]}, User: {credential["user"]})'
        LoggerUtil.logger.error(error_str, exc_info=True)
        if attempt < DbCredentials.retries:
            LoggerUtil.logger.info("Retrying Mysql Connection...")
            return create_mysql_connection(credential, attempt + 1)
        else:
            LoggerUtil.logger.fatal("MySQL connection failed 3 times. Giving up..", exc_info=True)
            raise


class DbConnector:

    def __init__(self, credentials):
        self.credentials = credentials
        self.connections = []
        self.create_connections()

    def create_connections(self):
        for cred in self.credentials:
            self.connections.append(create_mysql_connection(cred))
            LoggerUtil.logger.info(f"Connection to Host {cred['host']}, {cred['database']} Successful")

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.connections.clear()

    def reconnect(self):
        for connection in self.connections:
            connection.reconnect(attempts=DbCredentials.retries, delay=0)

    def get_connection(self):
        return random.choice(self.connections)

    def fetch_results_in_batch(self, query, batch_size, dictionary=False, try_again=True):
        rows = []
        try:
            connection = self.get_connection()
            connection.ping(True)
            with closing(connection.cursor(buffered=True, dictionary=dictionary)) as cursor:
                cursor.execute(query)
                if batch_size == -1:
                    rows = cursor.fetchall()
                else:
                    while True:
                        batch_empty = True
                        for row in cursor.fetchmany(batch_size):
                            batch_empty = False
                            rows.append(row)
                        if batch_empty:
                            break
            return rows
        except OperationalError as exception:
            LoggerUtil.logger.error(exception, exc_info=True)
            if try_again:
                self.reconnect()
                return self.fetch_results_in_batch(query, batch_size, dictionary, False)
            else:
                raise exception
