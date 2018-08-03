import re


class DwhError(Exception):
    def __init__(self):
        super().__init__(self, self.message)


class ScriptPrepException(DwhError):
    def __init__(self, message, script):
        self.message = 'Preparation procedure failed with follow exception '\
                       + "\"" + message + "\"" + ' for ' + script
        # super().__init__(self, self.message)

    def __str__(self):
        return self.message


class SqlPlusExecutionException(DwhError):
    def __init__(self, message, table):

        search = re.search(r'.*ORA.*', message.decode("utf-8"))
        if search:
            mess = search.group(0).strip()
        else:
            mess = 'UNKHOWN'
        self.message = "Extract procedure failed for " + table + " with sqlplus error: " + "\"" + mess + "\""
        # super().__init__(self, self.message)

    def __str__(self):
        return self.message


class RowsCountMismatch(DwhError):
    def __init__(self, table):
        self.message = "Count of rows in data file and control sum mismatch for " + table + " table"
        # super().__init__(self, self.message)

    def __str__(self):
        return self.message
