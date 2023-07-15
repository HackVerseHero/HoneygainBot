import os

from honey_pot_auto import HoneypotCatchBot
from Database.sqlite import SQLiteStorage

USER = os.environ['HONEYGAIN_USER']
PASS = os.environ['HONEYGAIN_PASS']

database_file = os.path.join("Storage", "data.db")

storage = SQLiteStorage(database_file)
hg = HoneypotCatchBot(USER, PASS, storage)

