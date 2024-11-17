# This file contains the error log class, a singleton

import os
import datetime

class ErrorLogger:
    def __init__(self):
        self.log_folder = 'error_logs'
        self.log_file = self._get_log_file_path()
        self._ensure_log_folder()

    def _ensure_log_folder(self):
        '''
        This function ensure the error log folder exists
        '''
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

    def _get_log_file_path(self):
        '''
        This function creates a log file path with a timestamp
        '''
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        return os.path.join(self.log_folder,f"error_log_{timestamp}.txt")

    def log_error(self, error_message):
        '''
        This function writes the error message to the log file
        '''
        with open(self.log_file, "a") as log_file:
            log_file.write(f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}] {error_message}\n")