import os

from honey_pot_auto import HoneypotCatchBot
from Database.sqlite import SQLiteStorage

USER = os.environ['HONEYGAIN_USER']
PASS = os.environ['HONEYGAIN_PASS']

dir_name = 'Storage'
if not os.path.exists(dir_name):
    os.mkdir(dir_name)
database_file = os.path.join(dir_name, 'data.db')

storage = SQLiteStorage(database_file)
hg = HoneypotCatchBot(USER, PASS, storage)

