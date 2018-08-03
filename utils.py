import json
import os
import re
import uuid
import subprocess
import gzip
import shutil


class Utils():

    @staticmethod
    def create_session_uuid():
        return str(uuid.uuid4())

    @staticmethod
    def file_row_count(file):
        p = subprocess.Popen(['wc', '-l', str(file)], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        result, err = p.communicate()
        if p.returncode != 0:
            raise IOError(err)
        return int(result.strip().split()[0])

    @staticmethod
    def gzip(file):
        gzip_file = file + '.gzip'
        with open(file, 'rb') as f_in:
            with gzip.open(gzip_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        return gzip_file

    @staticmethod
    def get_listdict_from_cur(cur):
        col_names = [desc[0] for desc in cur.description]
        rows = []
        for row in cur.fetchall():
            rw = {}
            for name, value in zip(col_names, row):
                rw[name] = value
            rows.append(rw)
        return rows
