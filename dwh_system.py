import os
import logging
from datetime import datetime
from pathlib import Path
from collections import namedtuple
import psycopg2
from utils import Utils


DataSourceInfo = namedtuple("DataSourceInfo",
                               ["name", "db_sid", "db_host", "db_pass", "db_port", "db_user", "tns", "code"])

DataTableInfo = namedtuple("DataTable", ["code", "name", "script_template"])



class DwhSystem:
    def __init__(self, source_code):
        # getting all paths and making needed dirs
        self.tmp_dir = Path(os.getenv("DWH_TMP_DIR"))
        self.logs_dir = Path(os.getenv("DWH_LOGS_DIR"))
        self.data_dir = Path(os.getenv("DWH_DATA_DIR"))
        self.work_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.sql_tmpl_dir = Path(os.path.join(self.work_dir, 'sql'))

        self.source_code = source_code

        # getting data source info
        ds_dict = self._get_data_source_info(source_code)
        self.data_source_info = DataSourceInfo(ds_dict["name"], ds_dict["db_sid"], ds_dict["db_host"],
                                               ds_dict["db_pass"], ds_dict["db_port"], ds_dict["db_user"],
                                               ds_dict["tns"], ds_dict["code"])

        dt_dict = self.get_tables_info(source_code)
        self.data_tables = []
        for tb in dt_dict:
            self.data_tables.append(DataTableInfo(tb["code"], tb["name"], tb["script_template"]))


        # making some needed paths
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.logs_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        # getting unique id for session
        self.session_uuid = Utils.create_session_uuid()

        # logger settings
        self.logger = logging.getLogger('DwhProcess:' + source_code + ":" + self.session_uuid)
        self.logger.setLevel(logging.DEBUG)

        file_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        log_file = datetime.today().strftime('%Y%m') + '.log'
        file_handler = logging.FileHandler(Path(self.logs_dir) / log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(file_formatter)

        console_formatter = logging.Formatter('%(asctime)s  %(message)s')

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(console_formatter)

        self.logger.addHandler(console)
        self.logger.addHandler(file_handler)

    def _get_connect(self):
        host = os.environ["DWH_DB_HOST"]
        db_name = os.environ["DWH_DB_NAME"]
        user = os.environ["DWH_DB_USER"]
        password = os.environ["DWH_DB_PASS"]

        conn = psycopg2.connect("host={} dbname={} user={} password={}".
                                format(host, db_name, user, password))
        return conn

    def _get_data_source_info(self, code):

        conn = self._get_connect()
        cur = conn.cursor()
        sql = """select 
                    ds.code,
                    ds.name,
                    ds.conn_detail,
                    ds.conn_detail ->> 'db_sid' as db_sid,
                    ds.conn_detail ->> 'db_pass' as db_pass,
                    ds.conn_detail ->> 'db_port' as db_port,
                    ds.conn_detail ->> 'db_user' as db_user,
                    ds.conn_detail ->> 'db_host' as db_host,
                    ds.tns                     
                 from sys.data_source ds 
                 where code = %s"""
        cur.execute(sql, (code, ))
        ds_dict = Utils.get_listdict_from_cur(cur)[0]
        return ds_dict

    def get_tables_info(self, code):
        conn = self._get_connect()
        cur = conn.cursor()
        sql = """
                select dstb.name,
                       dstb.code,
                       dstb.script_template
                from sys.data_source ds,
                     sys.data_source_table dstb,
                     sys.data_source_type dstp
                where
                    dstb.data_source_type_id = dstp.data_source_type_id and
                    ds.data_source_type_id = dstb.data_source_type_id and
                    ds.code = %s
                """
        cur.execute(sql, (code, ))
        dt_dict = Utils.get_listdict_from_cur(cur)
        return dt_dict
