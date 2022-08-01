import os


class Database:
    falcon = []
    rio = []
    bazooka1 = []
    bazooka2 = []
    bazooka3 = []
    mongo = None
    retries = 3

    def set_falcon_credentials(self):
        falcon_hosts = os.environ.get("FALCON_HOSTS").split(",")
        falcon_user = os.environ.get("FALCON_USER")
        falcon_pass = os.environ.get("FALCON_PASSWORD")
        falcon_database = os.environ.get("FALCON_DB_NAME")
        #LoggerUtil.logger.info("read Falcon connection from env")
        for host in falcon_hosts:
            self.falcon.append({
                "host": host,
                "user": falcon_user,
                "password": falcon_pass,
                "database": falcon_database
            })
        return None

    def set_rio_credentials(self):
        rio_hosts = os.environ.get("RIO_HOSTS").split(",")
        rio_user = os.environ.get("RIO_USER")
        rio_pass = os.environ.get("RIO_PASSWORD")
        rio_database = os.environ.get("RIO_DB_NAME")
        #LoggerUtil.logger.info("read rio connection from env")
        for host in rio_hosts:
            self.rio.append({
                "host": host,
                "user": rio_user,
                "password": rio_pass,
                "database": rio_database
            })
        return None

    def set_mongo_credentials(self):
        self.mongo = os.environ.get("MDB_CONN_STRING")
        return None


    def __init__(self):
        #self.set_falcon_credentials()
        #self.set_rio_credentials()
        self.set_mongo_credentials()

        # retries = int(os.environ.get("DB_RETRIES"))
        # if retries is not None:
        #     self.retries = retries


DbCredentials = Database()
