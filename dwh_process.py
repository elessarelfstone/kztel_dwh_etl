import os
import re
from pathlib import Path
import logging
import datetime
from datetime import datetime, timedelta
import settings
from utils import Utils
from dwh_system import DwhSystem


class DwhProcess():
    def __init__(self, dwh_sys,  params):
        self.dwh_sys = dwh_sys
        self.params = params

    def get_session_uuid(self):
        return self.dwh_sys.session_uuid

    def check_uuid(self, path):
        """

        Gets first line from file, obtains uuid and checks whether valid it or not
        :param path: path of a file
        :return: boolean of checking on right uuid
        """
        # TODO test this
        with open(path, "r", encoding="utf-8") as fh:
            uuid_line = fh.readline()
        search = re.search("^--.*", uuid_line)
        if search:
            uuid = search.group(0)[2:].strip()
            if uuid != self.dwh_sys.session_uuid:
                return
            else:
                return True
        else:
            return

