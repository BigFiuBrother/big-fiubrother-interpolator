import big_fiubrother_core.db.helper as db_helper
from os import path
import yaml


def configuration():
    with open(path.join(path.dirname(__file__), 'config', 'test.yml')) as file:
        return yaml.safe_load(file)


def set_up():
    db_helper.create(**configuration()['db'])


def tear_down():
    db_helper.drop(**configuration()['db'])
