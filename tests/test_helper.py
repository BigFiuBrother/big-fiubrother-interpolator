import big_fiubrother_core.db.helper as db_helper
from big_fiubrother_core import StoppableThread
from contextlib import contextmanager
from os import path
import yaml


def configuration():
    with open(path.join('config', 'test.yml')) as file:
        return yaml.safe_load(file)


@contextmanager
def start_task(task):
    thread = StoppableThread(task)
    thread.start()
    
    yield

    thread.stop()
    thread.wait()

    if thread.error is not None:
        raise Exception(thread.error)


def set_up():
    db_helper.create(**configuration()['db'])


def tear_down():
    db_helper.drop(**configuration()['db'])
