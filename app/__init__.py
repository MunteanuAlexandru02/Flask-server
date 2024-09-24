"""Used Flask for the ws, data_ingestor to access the csv and ThreadPool to time tasks"""
import math
import logging
import time
import threading
import os
from logging.handlers import RotatingFileHandler
import pandas
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPool()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.job_counter = 0
webserver.job_dictionary = {}

# Check if the folder exists
if not os.path.exists('results'):
    os.makedirs('results')

# Used to keep the last run of certain apis
webserver.prev_runs = {}

webserver.logger = logging.getLogger(__name__)
webserver.logger.setLevel(logging.INFO)

class TimeFormatter(logging.Formatter):
    """Class that modifies local time into GMT"""
    converter = time.gmtime

gmt_formatter = TimeFormatter("%(asctime)s : %(levelname)s : %(message)s")

rotating_file = RotatingFileHandler('webserver.log', maxBytes = 3*1024*1024, backupCount = 5)
rotating_file.setLevel(logging.INFO)
rotating_file.setFormatter(gmt_formatter)

webserver.logger.addHandler(rotating_file)

#server will be running by default
webserver.running = True

# Replies samples
webserver.shut_down = { 'job_id': -1, 'reason': "shutting down" }
webserver.reply_to_request = {'status': 'done', 'job_id': 0}
webserver.shutting_down = {"status": "done", "result": "server is shutting down"}

webserver.job_lock = threading.Lock()
webserver.counter_lock = threading.Lock()
webserver.reply_lock = threading.Lock()

from app import routes
