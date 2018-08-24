from subprocess import Popen, PIPE
from pathlib import Path
import time
from dwh_process import DwhProcess
import decorators
from exceptions import *
from utils import Utils
from dwh_script import DwhScript


class DwhOracleTable(DwhProcess):
    def __init__(self, dwh_sys, params):
        super(DwhOracleTable, self).__init__(dwh_sys, params)
        self.tns_conn_str = "{}/{}@{}".format(self.dwh_sys.data_source_info.db_user,
                                              self.dwh_sys.data_source_info.db_pass,
                                              self.dwh_sys.data_source_info.tns)
        self.script_handler = DwhScript(dwh_sys)

    def _save_table_data_by_sqlplus(self, script_path):
        """
        Run extract script for a certain table and then sqlplus by itself save data in csv
        :param table: target table
        :return: output information given by sqlplus
        """
        script = '@' + script_path.read_text(encoding="utf8")
        command = self.tns_conn_str
        session = Popen(["sqlplus", "-S", command], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        session.stdin.write(script.encode())
        out, err = session.communicate('\n exit;'.encode())
        return session.returncode, err, out

    def save_table_data(self, table, day):
        """
        :param table: table which data is being retrieved and saved
        :return: flag that indicate how it has done, csv file rows count, value from crc file
        """

        try:
            success = False
            self.dwh_sys.logger.info("Date - " + day.strftime("%Y-%m-%d"))
            start = time.time()
            script, csv, crc = self.script_handler.prepare_script_for_sqlplus(table, day)
            return_code, err, out = self._save_table_data_by_sqlplus(script)
            if return_code != 0:
                raise SqlPlusExecutionException(out, table.code)

            rows_real_count = Utils.file_row_count(csv)
            crc_rows_count = int(Path(crc).read_text().strip())
            if rows_real_count == crc_rows_count:
                success = True
                gzip_file = Utils.gzip(str(csv))
                Path(csv).unlink()
                self.dwh_sys.logger.info("Data successfully extracted in " + gzip_file)
            else:
                raise RowsCountMismatch(table)
            end = time.time()
            self.dwh_sys.logger.debug("Elapsed time : {} minutes {} seconds".format(divmod(end-start, 60)[0], int(divmod(end-start, 60)[1])))
            self.dwh_sys.logger.debug("csv rows count:{} check sum:{}".format(rows_real_count, crc_rows_count) + "\n")
            return success, gzip_file, rows_real_count, crc_rows_count
        except DwhError as e:
            self.dwh_sys.logger.error(e)



