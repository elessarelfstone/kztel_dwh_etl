import dwh_oracle_extract
import dwh_system
import collections
import settings

dwh_sys = dwh_system.DwhSystem("asr_astana")
for name, value in dwh_sys.data_source_info._asdict().items():
    print(name, "=", value)

dwh = dwh_oracle_extract.DwhOracleExtract(dwh_sys, {"pDate1": "02.08.2018", "pDate2": "02.08.2018"})
dwh.save_data()
