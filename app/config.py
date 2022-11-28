import os

class DbConnect:
    falcon = []
    bazookadb1 = []
    user = None
    password = None
    db_name = None

    def __init__(self):
        # self.set_falcon_credentials()
        self.set_bazooka_db1_credentials()

    def set_bazooka_db1_credentials(self):
        hosts = os.environ.get("BAZOOKADB1_HOSTS").split(",")
        user = os.environ.get("BAZOOKADB1_USER")
        password = os.environ.get("BAZOOKADB1_PASSWORD")
        db_name = os.environ.get("BAZOOKADB1_DB_NAME")

        for host in hosts:
            self.bazookadb1.append({
                "host": host,
                "user": user,
                "password": password,
                "database": db_name
            })

    def set_falcon_credentials(self):
        hosts = os.environ.get("FALCON_HOSTS").split(",")
        user = os.environ.get("FALCON_USER")
        password = os.environ.get("FALCON_PASSWORD")
        db_name = os.environ.get("FALCON_DB_NAME")

        for host in hosts:
            self.falcon.append({
                "host": host,
                "user": user,
                "password": password,
                "database": db_name
            })

    def get_host(self):
        return self.host

    def get_user(self):
        return self.user

    def get_password(self):
        return self.password

    def get_db_name(self):
        return self.db_name

DB_CREDENTIALS = DbConnect()


feature_id_map = {
                        1: "similar profiles",
                        2: "full resume text",
                        3: "some other service"
                      }