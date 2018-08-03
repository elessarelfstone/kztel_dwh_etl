import dwh_oracle_table
import dwh_system
import settings
import utils
import exceptions



# uralsk_data_source = {"source_name": "АСР БИТТЛ ЗКО",
#                       "code": "asr_uralsk",
#                       "db_user": "reporter",
#                       "db_pass": "ciuyrhvv",
#                       "tns": "(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=10.71.200.15)(PORT=1521)))(CONNECT_DATA=(SERVICE_NAME=URALASR.weskaz)))"}
#
# uralsk_data_source = {"source_name": "АСР БИТТЛ ЗКО",
#                       "code": "asr_aktobe",
#                       "db_user": "reporter",
#                       "db_pass": "ciuyrhvv",
#                       "tns": "(DESCRIPTION = (ADDRESS_LIST =  (ADDRESS = (PROTOCOL=TCP)(HOST=10.71.200.8)(PORT=1521)))(CONNECT_DATA = (SERVICE_NAME=aktoasr.Aktobe)))"}



dwh_sys = dwh_system.DwhSystem("asr_uralsk")
# data_sources = dwh_sys.get_data_sources()


dwh = dwh_oracle_table.DwhOracleTable(dwh_sys,  {"pDate1": "01.07.2018"})
dwh.save_table_data("tdr")
