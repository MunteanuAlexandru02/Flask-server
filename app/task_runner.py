"""Used ThreadPoolExecutor from concurrent.features to avoid the implementaion of a custom TP"""
from concurrent.futures import ThreadPoolExecutor
import os

class ThreadPool:
    """Creates a ThreadPool using the ThreadPoolExecutor from concurrent.futures"""
    def __init__(self):
        self.number_threads = self.get_number_threads()
        self.tp_executor = ThreadPoolExecutor(max_workers=self.number_threads)

    def get_number_threads(self):
        """Method to check if the env variable exists"""
        if 'TP_NUM_OF_THREADS' in os.environ:
            return int(os.environ('TP_NUMBER_OF_THREADS'))

        cpu_count = os.cpu_count()

        if cpu_count is None:
            return 1
        return cpu_count
