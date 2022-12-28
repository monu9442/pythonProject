import os
FALCON_NAME = 'falcon'
BAZOOKA_NAME = 'bazooka'
RIO_NAME = 'rio'

# PROD
FALCON_HOST = '172.30.10.10'
FALCON_USER = 'Akhileshn'
FALCON_PASS = '@kh!le$hnwert'
BAZOOKA_HOST = '172.30.10.24'
BAZOOKA_PASS = '@kh!le$hnwert'
BAZOOKA_USER = 'Akhileshn'
RIO_HOST = '172.30.10.52'
RIO_USER = 'Akhileshn'
RIO_PASS = '@kh!le$hnwert'

# QA
# FALCON_HOST =
# FALCON_USER =
# FALCON_PASS =
# BAZOOKA_HOST =
# BAZOOKA_PASS =
# BAZOOKA_USER =
# BAZOOKA_NAME =
# RIO_HOST =
# RIO_USER =
# RIO_PASS =


class Database:
    falcon = []
    rio = []
    bazooka1 = []
    bazooka2 = []
    bazooka3 = []
    retries = 3

    def set_falcon_credentials(self):
        falcon_hosts = FALCON_HOST
        falcon_user = FALCON_USER
        falcon_pass = FALCON_PASS
        falcon_database = FALCON_NAME
        print("read Falcon connection from env")
        for host in falcon_hosts:
            self.falcon.append({
                "host": host,
                "user": falcon_user,
                "password": falcon_pass,
                "database": falcon_database
            })
        return None

    def set_rio_credentials(self):
        rio_hosts = RIO_HOST
        rio_user = RIO_USER
        rio_pass = RIO_PASS
        rio_database = RIO_NAME
        print("read rio connection from env")
        for host in rio_hosts:
            self.rio.append({
                "host": host,
                "user": rio_user,
                "password": rio_pass,
                "database": rio_database
            })
        return None

    def set_bazooka_credentials(self):
        bazookadb_host = BAZOOKA_HOST
        bazookadb_user = BAZOOKA_USER
        bazookadb_pass = BAZOOKA_PASS
        bazooka_databases = BAZOOKA_NAME
        print("reading Bazooka connection from env......")
        for host in bazookadb_host:
            self.bazooka2.append({
                "host": host,
                "user": bazookadb_user,
                "password": bazookadb_pass,
                "database": bazooka_databases
            })
        return None


    def __init__(self):
        self.set_falcon_credentials()
        self.set_rio_credentials()
        self.set_bazooka_credentials()


DbCredentials = Database()
