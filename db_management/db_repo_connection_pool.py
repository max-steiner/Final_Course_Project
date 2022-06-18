import time
import threading
from db_management.db_repo import DbRepo
from db_management.db_config import local_session, config


class DbRepoConnectionPool(object):
    _instance = None
    _lock = threading.Lock()
    _lock_pool = threading.Lock()
    _max_connections = int(config["limits"]["max_conn"])

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def get_instance(cls):
        if cls._instance: return cls._instance
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls.__new__(cls)
                cls._instance.connections = [DbRepo(local_session) for i in range(cls._max_connections)]
            return cls._instance

    def get_free_count(self):
        return len(self.connections)

    def get_max_possible_connections(cls):
        return cls._max_connections

    def get_connection(self):
        while True:
            if len(self.connections) == 0:
                time.sleep(1 / 2)
                continue
            with self._lock_pool:
                if len(self.connections) > 0: return self.connections.pop(0)

    def return_connection(self, conn):
        with self._lock_pool: self.connections.append(conn)