import tempfile
import logging
import os

_logger = logging.getLogger(__name__)

class TempFileManager:
    def __init__(self, app_subdir_name="gaidme"):
        system_temp_dir = tempfile.gettempdir()
        self.base_dir = os.path.join(system_temp_dir, app_subdir_name)
        directory_already_exists = os.path.exists(self.base_dir)
        os.makedirs(self.base_dir, exist_ok=True)
        self.files = {}
        _logger.debug(f"Application's temporary directory: {self.base_dir}")
        os.environ['GAIDME_BASE_DIR'] = self.base_dir

        if directory_already_exists:
            self._populate_existing_files()

    def _populate_existing_files(self):
        """
        Populates self.files with existing files in the base directory.
        """
        for filename in os.listdir(self.base_dir):
            filepath = os.path.join(self.base_dir, filename)
            if os.path.isfile(filepath):
                self.files[filename] = filepath
                _logger.debug(f"File {filename} already exist")

    def create(self, filename: str, content: str):
        """
        Creates a file with the given filename and content in the application's temporary directory.
        """
        filepath = os.path.join(self.base_dir, filename)
        with open(filepath, 'w') as tmpfile:
            tmpfile.write(content)
        self.files[filename] = filepath
        _logger.debug(f'File {filename} created at: {filepath}')

    def read(self, filename: str) -> str:
        """
        Reads and returns the content of the specified file from the application's temporary directory.
        """
        filepath = self.files.get(filename)
        if not filepath or not os.path.exists(filepath):
            raise FileNotFoundError(f"No such file: {filename}")
        
        with open(filepath, 'r') as tmpfile:
            return tmpfile.read()

    def cleanup(self, filename: str = None):
        """
        Cleans up a specific temporary file or all temporary files in the directory if no filename is provided.
        """
        if filename:
            filepath = self.files.pop(filename, None)
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                _logger.debug(f"File {filename} cleaned up.")
        else:
            for filename, filepath in self.files.items():
                if os.path.exists(filepath):
                    os.remove(filepath)
                    _logger.debug(f"File {filename} cleaned up.")
            self.files.clear()
            _logger.debug("All temporary files cleaned up.")

TempFile = TempFileManager()