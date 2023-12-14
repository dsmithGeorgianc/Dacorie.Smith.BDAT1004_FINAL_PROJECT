# settings.py
import os

from dotenv import load_dotenv


class Setting:

    def __init__(self):
        self.load_env_setting()

    def load_env_setting(self):
        load_dotenv()

        # OR, the same with increased verbosity
        load_dotenv(verbose=True)

        # OR, explicitly providing path to '.env'
        from pathlib import Path  # Python 3.6+ only
        env_path = Path('.') / '.env'
        load_dotenv(dotenv_path=env_path)

    def get_env(self, key):
        return os.getenv(key)
