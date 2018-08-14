from dwh_oracle_table import DwhProcess


class DwhOracleExtract(DwhProcess):
    def __init_(self, dwh_sys, params):
        self._data_source = dwh_sys.get_data_source()

    def get_all_tables(self):


    def extract_data(self):
