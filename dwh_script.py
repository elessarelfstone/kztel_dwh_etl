from pathlib import Path
from exceptions import ScriptPrepException


class DwhScript:
    main_template = "main.sqtmpl"
    csv_name_format = "{}_{}.csv"
    crc_name_format = "{}_{}.crc"

    def __init__(self, dwh_sys):
        self.dwh_sys = dwh_sys

    def prepare_script_for_sqlplus(self, table, day):
        """
        Substitutes given input parameters for certain script
        and saves prepared sql-script in temp folder
        :param table: table is being extracted
        :param day: day that we are extracting data for
        :return: prepared sql-script path
        """
        # getting sqlplus headers and setting output csv filename in it
        try:
            template_file = self.dwh_sys.sql_tmpl_dir / self.main_template
            # getting path for output data file
            output_csv_file = self.dwh_sys.data_dir / self.dwh_sys.source_code / day.strftime('%Y%m') / self.csv_name_format.format(
                Path(table.code).stem,
                day.strftime("%Y%m%d"))

            # getting path for output crc(control sum) file
            output_crc_file = self.dwh_sys.data_dir / self.dwh_sys.source_code / day.strftime('%Y%m') / self.crc_name_format.format(
                Path(table.code).stem,
                day.strftime("%Y%m%d"))

            # read main template body
            template = template_file.read_text(encoding="utf8")

            # read template for table and put date there
            script_file = Path(self.dwh_sys.sql_tmpl_dir) / table.script_template
            script_body = script_file.read_text(encoding="utf8").format(pDate=day.strftime("%d.%m.%Y"))

            # put in main template paths for files and script for table
            script = template.format(output_csv_file, script_body, output_crc_file)
            # concatenate session uid and prepared script
            full_script = "\n".join(["--" + self.dwh_sys.session_uuid, script])

            # saving script in temp directory
            script_path = Path(self.dwh_sys.tmp_dir) / '{}.sql'.format(script_file.stem)
            script_path.write_text(full_script, encoding="utf8")
            return script_path, output_csv_file, output_crc_file
        except Exception as e:
            raise ScriptPrepException(str(e), table.code)
