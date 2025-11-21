import gzip
import shutil
import os
from logging.handlers import TimedRotatingFileHandler

import develop.constants as constants
from develop.supports_write import SupportsWrite


class CompressingTimedRotatingLogFileHandler(TimedRotatingFileHandler):

    @staticmethod
    def _try_compress(file: str)->bool:
        compressed_log_path: str = f"{file}{constants.EXTENSION_COMPRESSED_GZIP}"

        if os.path.isfile(file) and not os.path.exists(compressed_log_path):
            with open(file, mode=constants.FILE_MODE_READ_BINARY) as input_file:
                with gzip.open(compressed_log_path, mode=constants.FILE_MODE_WRITE_BINARY) as output_file:
                    output_file: SupportsWrite
                    shutil.copyfileobj(input_file, output_file)
            return True
        else:
            return False

    def doRollover(self):
        """Overrides the default log rotation to add gzip compression."""
        super().doRollover()

        folder: str = self.baseFilename.rsplit(sep=os.sep, maxsplit=1)[0]
        base_file_name: str = os.path.basename(self.baseFilename)
        for file in os.listdir(folder):
            if file.startswith(base_file_name) and not file.endswith(constants.EXTENSION_COMPRESSED_GZIP):
                old_log_path: str = os.path.join(folder, file)
                if self._try_compress(old_log_path):
                    os.remove(old_log_path)
