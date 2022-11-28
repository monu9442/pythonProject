import mysql.connector
from config.DbConnect import DB_CREDENTIALS
from utils.common.constant.SearchScope import SearchScope
from utils.common.constant.RecuriterScope import RecruiterScope
from utils.Logger import LoggerUtil
import random

feature_map = RecruiterScope.get_feature_id_map()

def create_mysql_connection(credential):
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
        LoggerUtil.logger.info("Retrying Mysql Connection...")


class DbConnect:
    REC_ACCESS_DATA_QUERY = "select rec_id, group_concat(feature_id) as feature_ids, group_concat(feature_name) as feature_name, group_concat(enabled) as enabled FROM recruiter_feature_access "
    X_CODE_QUERY = "SELECT xcode, id FROM corps WHERE xcode in "
    GROUP_BY_CLAUSE = " GROUP BY rec_id;"

    def __init__(self, credentials):
        self.credentials = credentials
        self.connections = []

    # def getDBConnect(self):
    #     db = mysql.connector.connect(host=SearchScope.DB_LOGIN["host"],
    #                                  user=SearchScope.DB_LOGIN["user"],
    #                                  passwd=SearchScope.DB_LOGIN["password"],
    #                                  db=SearchScope.DB_LOGIN["database"])
    #     return db

    def create_connections(self):
        for cred in self.credentials:
            self.connections.append(create_mysql_connection(cred))
            LoggerUtil.logger.info(f"Connection to Host {cred['host']}, {cred['database']} Successful...")

    def close_connections(self):
        for connection in self.connections:
            connection.close()
        self.connections.clear()

    def get_connection(self):
        return random.choice(self.connections)

    # def getCurrency(self):
    #     db = self.getDBConnect()
    #     __cursor = db.cursor()
    #     __sql_query = "SELECT currency_code, usd_price FROM currencies"
    #     __cursor.execute(__sql_query)
    #     __currency_mapping = dict(__cursor.fetchall())
    #     return __currency_mapping

    def get_recruiter_dict(self):
        try:
            self.create_connections()
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(self.REC_ACCESS_DATA_QUERY + "WHERE enabled = 1 GROUP BY rec_id")
            db_data = cursor.fetchall()
            rec_dict = self.create_dict_from_db_data(db_data)
            self.close_connections()
            return rec_dict
        except Exception as E:
            LoggerUtil.logger.error(f"Error in creating Recruiter Dict : {E}")
            return {}


    def create_dict_from_db_data(self, db_data):
        temp = dict()
        for data in db_data:
            temp[data[0]] = list(map(int, data[1].split(",")))
        return temp

    def update_rec_dict(self, form_data, recruiter_dict):
        for rec_id in form_data:
            for f_id in form_data.get(rec_id, []).get('enable', []):
                if int(rec_id) not in recruiter_dict:
                    recruiter_dict[int(rec_id)] = [f_id]
                else:
                    if f_id not in recruiter_dict.get(int(rec_id), []):
                        recruiter_dict.get(int(rec_id)).append(f_id)

        for rec_id in form_data:
            for f_id in form_data.get(rec_id, []).get('disable', []):
                if f_id in recruiter_dict.get(int(rec_id), []):
                    recruiter_dict.get(int(rec_id)).remove(f_id)
        return True

    def update_records_in_DB(self, list_of_ids, feature_id, access_type):
        if len(list_of_ids) > 0:
            self.create_connections()
            connection = self.get_connection()
            cursor = connection.cursor()
            id_string = ','.join(map(str,list_of_ids))
            query = f"UPDATE recruiter_feature_access SET enabled = {int(access_type)} " \
                    f"WHERE feature_id = {feature_id} AND rec_id in ({id_string})"
            cursor.execute(query)
            self.close_connections()
            LoggerUtil.logger.info(f"Recruiters access to feature modified to {access_type} for Recruiter IDS = {list_of_ids} ")

    def insert_recruiter_access_in_DB(self, list_of_ids, feature_id, access):
        if len(list_of_ids) > 0:
            self.create_connections()
            connection = self.get_connection()
            cursor = connection.cursor()
            query = "INSERT INTO recruiter_feature_access (rec_id, feature_id, feature_name, enabled) values "
            for id in list_of_ids:
                query += f"({id},{int(feature_id)},'{feature_map.get(feature_id)}', {int(access)}),"
            query = query[:-1]
            cursor.execute(query)
            self.close_connections()
            LoggerUtil.logger.info(f"Recruiters access to feature {feature_map[feature_id]} to {bool(access)}: {list_of_ids}")

    def get_access_change_data(self, form_data):
        enable = {}
        disable = {}

        for rec_id in form_data:
            if form_data.get(rec_id).get('enable'):
                for feature_id in form_data[rec_id].get("enable"):
                    if enable.get(feature_id):
                        enable[feature_id].append(int(rec_id))
                    else:
                        enable[feature_id] = [int(rec_id)]

            if form_data.get(rec_id).get('disable'):
                for feature_id in form_data[rec_id].get("disable"):
                    if disable.get(feature_id):
                        disable[feature_id].append(int(rec_id))
                    else:
                        disable[feature_id] = [int(rec_id)]

        return {
            "enable": enable,
            "disable": disable
        }

    def create_rec_dict_from_db(self, db_data):
        rec_dicts = {}
        for data in db_data:
            feature_ids = list(map(str, data[1].split(",")))
            access_type = list(map(int, data[3].split(",")))
            rec_acc_dict = dict(zip(feature_ids, access_type))
            rec_dicts.update({data[0]: rec_acc_dict})
        return rec_dicts

    def update_db(self,access_change_data, rec_ids):
        query = self.REC_ACCESS_DATA_QUERY+ f"WHERE rec_id in ({','.join(map(str,rec_ids))})" + self.GROUP_BY_CLAUSE
        self.create_connections()
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        db_data = cursor.fetchall()
        rec_dict_from_db = self.create_rec_dict_from_db(db_data)
        self.close_connections()

        enabled = access_change_data.get('enable', [])
        disable = access_change_data.get('disable', [])

        insertion_ids = []
        update_ids = []

        for feature_id in enabled:
            insertion_ids, update_ids = [], []
            for rec_id in enabled.get(feature_id):
                if str(feature_id) in rec_dict_from_db.get(rec_id, []):
                    update_ids.append(rec_id)
                elif feature_id in feature_map:
                    insertion_ids.append(rec_id)
            self.update_records_in_DB(update_ids, feature_id,True)
            self.insert_recruiter_access_in_DB(insertion_ids, feature_id, True)

        for feature_id in disable:
            insertion_ids = []
            update_ids = []
            for rec_id in disable.get(feature_id):
                if str(feature_id) in rec_dict_from_db.get(rec_id, []):
                    update_ids.append(rec_id)
                elif feature_id in feature_map:
                    insertion_ids.append(rec_id)
            self.update_records_in_DB(update_ids, feature_id, False)
            self.insert_recruiter_access_in_DB(insertion_ids, feature_id, False)


        return True

    def get_feature_map_template(self):
        temp = dict()
        for feature_id in feature_map:
            temp.update({feature_id:[]})
        return temp

    def get_enabled_disabled_list(self, form_data):
        enable = self.get_feature_map_template()
        disable = self.get_feature_map_template()
        for rec_id in form_data:
            for feature_id in form_data.get(rec_id).get('enable', None):
                enable[feature_id].append(rec_id)
            for feature_id in form_data.get(rec_id).get('disable', None):
                disable[feature_id].append(rec_id)
        return enable, disable

    def get_processed_form_data(self, form_data):
        xcodes = list(form_data.keys())
        db_data = self.get_rec_ids_from_bazooka(xcodes)
        temp = dict()
        for data in db_data:
            if data[0] in form_data:
                temp[str(data[1])] = form_data[data[0]]

        return temp

    def get_rec_ids_from_bazooka(self, list_of_x_codes):
        in_bracket_value = ""
        for xcode in list_of_x_codes:
            in_bracket_value += "'" + xcode + "',"
        in_bracket_value = in_bracket_value[:-1]
        query = self.X_CODE_QUERY + f"({in_bracket_value});"
        self.create_connections()
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        db_data = cursor.fetchall()
        self.close_connections()
        return db_data

DbConnect = DbConnect(DB_CREDENTIALS.bazookadb1)