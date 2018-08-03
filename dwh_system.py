import psycopg2
import settings
import os
import json
import logging
from utils import Utils
from datetime import datetime
from pathlib import Path


class DwhSystem():
    def __init__(self, source_code):
        self.tmp_dir = os.getenv("DWH_TMP_DIR")
        self.logs_dir = os.getenv("DWH_LOGS_DIR")
        self.data_dir = os.getenv("DWH_DATA_DIR")
        self.work_dir = os.path.dirname(os.path.abspath(__file__))
        self.sql_tmpl_dir = os.path.join(self.work_dir, 'sql')

        self.data_source = self._get_data_source(source_code)

        # making some needed paths
        Path(self.tmp_dir).mkdir(parents=True, exist_ok=True)
        Path(self.logs_dir).mkdir(parents=True, exist_ok=True)
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)

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

    def _get_data_source(self, code):
        host = os.environ["DWH_DB_HOST"]
        dbname = os.environ["DWH_DB_NAME"]
        user = os.environ["DWH_DB_USER"]
        password = os.environ["DWH_DB_PASS"]

        conn = psycopg2.connect("host={} dbname={} user={} password={}".
                                format(host, dbname, user, password))

        cur = conn.cursor()
        sql = "select * from sys.data_source where code = %s"
        cur.execute(sql, (code, ))
        result = Utils.get_listdict_from_cur(cur)[0]
        conn_detail = result["conn_detail"]
        result.update(conn_detail)
        result.pop("conn_detail")
        return result








