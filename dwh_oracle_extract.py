from dwh_process import DwhProcess
from dwh_oracle_table import DwhOracleTable
from datetime import datetime
import datetime as dt
from pathlib import Path


class DwhOracleExtract(DwhProcess):
    def __init__(self, dwh_sys, params):
        super(DwhOracleExtract, self).__init__(dwh_sys, params)
        self.dates = self._get_dates()
        data_months = list(set([d.strftime("%Y%m") for d in self.dates]))
        # create folder for a month, which will be contain its days data
        for month in data_months:
            data_dir = Path(self.dwh_sys.data_dir) / self.dwh_sys.data_source_info.code / month
            data_dir.mkdir(parents=True, exist_ok=True)
        self.data_handler = DwhOracleTable(dwh_sys, params)

    def _get_dates(self):
        pdate1 = datetime.strptime(self.params["pDate1"], "%d.%m.%Y")
        pdate2 = datetime.strptime(self.params["pDate2"], "%d.%m.%Y")
        return [pdate1 + dt.timedelta(n) for n in range(int((pdate2 - pdate1).days)+1)]

    def save_data(self):
        for table in self.dwh_sys.data_tables:
            self.dwh_sys.logger.info("Data extraction started for " + table.code + " table")
            for day in self.dates:
                self.data_handler.save_table_data(table, day)
            self.dwh_sys.logger.info("Data extraction ended for " + table.code + " table")
