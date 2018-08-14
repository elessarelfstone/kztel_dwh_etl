import dwh_oracle_table
import dwh_system



dwh_sys = dwh_system.DwhSystem("asr_uralsk")
dwh = dwh_oracle_table.DwhOracleTable(dwh_sys,  {"pDate1": "16.07.2018"})
dwh.save_table_data("tdr")
dwh.save_table_data("payment")


dwh_sys = dwh_system.DwhSystem("asr_aktobe")
dwh = dwh_oracle_table.DwhOracleTable(dwh_sys,  {"pDate1": "16.07.2018"})
dwh.save_table_data("tdr")
dwh.save_table_data("payment")