from subprocess import Popen, PIPE
from pathlib import Path
from datetime import datetime
from dwh_process import DwhProcess
import decorators
from exceptions import *
from utils import Utils


class DwhOracleTable(DwhProcess):
    def __init__(self,dwh_sys, params):
        super(DwhOracleTable, self).__init__(dwh_sys, params)
        self.template_suffix = ".sqtmpl"
        self.main_template = "main.sqtmpl"
        self.tns_conn_str = "{}/{}@{}".format(self.dwh_sys.data_source["db_user"],
                                              self.dwh_sys.data_source["db_pass"],
                                              self.dwh_sys.data_source["tns"])
        self.csv_name_format = "{}_{}.csv"
        self.crc_name_format = "{}_{}.crc"

        self.date = datetime.strptime(self.params["pDate1"], "%d.%m.%Y")

        # create folder for a month, which will be contain its days data
        data_dir = Path(self.dwh_sys.data_dir) / self.dwh_sys.data_source["code"] / self.date.strftime('%Y%m')
        data_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir = data_dir

    def _prepare_script_for_sqlplus(self, script_name):
        """
        Substitutes given input parameters for certain script
        and saves prepared sql-script in temp folder
        :param script_name: sql template, for example tdr.sqtmpl
        :return: prepared sql-script path
        """
        # getting sqlplus headers and setting output csv filename in it
        try:
            template_file = Path(self.dwh_sys.sql_tmpl_dir) / self.main_template
            output_csv_file = self.data_dir / self.csv_name_format.format(Path(script_name).stem,
                                                                          self.date.strftime("%Y%m%d"))
            output_crc_file = self.data_dir / self.crc_name_format.format(Path(script_name).stem,
                                                                          self.date.strftime("%Y%m%d"))
            template = template_file.read_text(encoding="utf8")

            script_file = Path(self.dwh_sys.sql_tmpl_dir) / script_name
            script_body = script_file.read_text(encoding="utf8").format(**self.params)

            script = template.format(output_csv_file, script_body, output_crc_file)

            full_script = "\n".join(["--" + self.dwh_sys.session_uuid, script])

            # saving script in temp directory
            script_path = Path(self.dwh_sys.tmp_dir) / '{}.sql'.format(script_file.stem)
            script_path.write_text(full_script, encoding="utf8")
            return script_path, output_csv_file, output_crc_file
        except Exception as e:
            raise ScriptPrepException(str(e), script_name)

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

    @decorators.timeit("mins")
    def save_table_data(self, table):
        """
        :param table: table which data is being retrieved and saved
        :return: flag that indicate how it has done, csv file rows count, value from crc file
        """

        #TODO предусмотреть выгрузку данных за несколько дней назад

        try:
            success = False
            self.dwh_sys.logger.info("Data extraction started for " + table + " table")
            script_name = table + self.template_suffix
            script, csv, crc = self._prepare_script_for_sqlplus(script_name)
            return_code, err, out = self._save_table_data_by_sqlplus(script)
            if return_code != 0:
                raise SqlPlusExecutionException(out, table)

            rows_real_count = Utils.file_row_count(csv)
            crc_rows_count = int(Path(crc).read_text().strip())
            if rows_real_count == crc_rows_count:
                success = True
                gzip_file = Utils.gzip(str(csv))
                self.dwh_sys.logger.info("Data extraction successfully ended for " + table + " table")
            else:
                raise RowsCountMismatch(table)
            self.dwh_sys.logger.debug("csv rows count:{} check sum:{}".format(rows_real_count, crc_rows_count))
            return success, gzip_file, rows_real_count, crc_rows_count
        except DwhError as e:
            self.dwh_sys.logger.error(e)
