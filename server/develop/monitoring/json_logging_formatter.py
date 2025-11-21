import json
import logging

import develop.constants as constants


class JsonLoggingFormatter(logging.Formatter):
    def format(self, record):
        if isinstance(record.msg, dict):
            record.msg = json.dumps(record.msg, indent=constants.INDENT_JSON)
            record.args = ()
        return super().format(record)
