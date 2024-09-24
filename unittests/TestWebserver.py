"""Unittest file"""
import unittest
import os
import pandas as pd
from deepdiff import DeepDiff
import app.replies as rp
from app.data_ingestor import DataIngestor

class TestWebserver(unittest.TestCase):
    """"Class for unittests"""
    def setUp(self):
        # Remove the files from results
        os.system("rm -rf results/*")

        self.test_job_id = 'job_id_1'

        self.test_dict = {'question': ['Ce faci', 'Mergem la curs'],
                            'state': ['Arges', 'Bucuresti']}

        self.ingestor = DataIngestor('./test_data.csv')

        self.data = pd.read_csv("./test_data.csv")

        #states_mean_reply with 'Ce faci' as question
        self.states_mean_res = {'Bucuresti': 16.75, 'Arges': 36.233}

        #state_mean_reply with 'Ce faci' as question and 'Arges' as state
        self.state_mean_res = {'Arges': 36.233}

        #best5_reply with 'Ce faci' as question
        self.best5_res = {'Arges': 36.233, 'Bucuresti': 16.75}

        #worst5_reply with 'Ce faci' as question
        self.worst5_res = {'Bucuresti': 16.75, 'Arges': 36.233}

        #global_mean with 'Mergem la curs' as question
        self.global_res = {'global_mean': 46.975}

        #diff_from_mean with 'Mergem la curs' as question
        self.diff_from_mean_res = {'Arges': 8.175, 'Bucuresti': -8.175}

        #state_diff with 'Mergem la curs' as question
        self.state_diff_res = {'Bucuresti': -8.175}

        #mean_by_category with 'Mergem la curs' as question
        self.mean_by_cat_res = {"('Arges', 'idk2', 'susanu')": 22.5,
                                "('Arges', 'idk2', 'mr juve')": 55.1,
                                "('Bucuresti', 'idk2', 'liverpool')": 88.2,
                                "('Bucuresti', 'idk1', 'liverpool')": 22.1}

        #state_mean_by_category with 'Ce faci' as question
        self.state_mean_by_cat_res = {'Arges': {"('idk1', 'susanu')": 37.8,
                                        "('idk1', 'mr juve')": 33.1}}


    def test_states_mean(self):
        """Test states mean"""
        values = rp.states_mean_reply(self.test_job_id, self.test_dict['question'][0],
                                        self.ingestor)
        d = DeepDiff(values, self.states_mean_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed states_mean")

    def test_state_mean(self):
        """Test state mean"""
        values = rp.state_mean_reply(self.test_job_id, self.test_dict['question'][0],
                                     self.test_dict['state'][0], self.ingestor)
        d = DeepDiff(values, self.state_mean_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed state_mean")

    def test_best5(self):
        """Test best5"""
        values = rp.best5_reply(self.test_job_id, self.test_dict['question'][0], self.ingestor)
        d = DeepDiff(values, self.best5_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed best5")

    def test_worst5(self):
        """Test worst5"""
        values = rp.worst5_reply(self.test_job_id, self.test_dict['question'][0], self.ingestor)
        d = DeepDiff(values, self.worst5_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed worst5")

    def test_global_mean(self):
        """Test global mean"""
        values = rp.global_mean_reply(self.test_job_id,
                    self.test_dict['question'][1], self.ingestor)
        d = DeepDiff(values, self.global_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed global mean")

    def test_state_diff_from_mean(self):
        """Test the state diff from mean"""
        values = rp.state_diff_from_mean_reply(self.test_job_id, self.test_dict['question'][1],
                                            self.test_dict['state'][1], self.ingestor)
        values[self.test_dict['state'][1]] = float(values[self.test_dict['state'][1]])
        d = DeepDiff(values, self.state_diff_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed state diff from mean")

    def test_mean_by_category(self):
        """Test the mean by category"""
        values = rp.mean_by_category_reply(self.test_job_id,
                        self.test_dict['question'][1], self.ingestor)
        d = DeepDiff(values, self.mean_by_cat_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed mean by category")

    def test_state_mean_by_category(self):
        """Test the state mean by category"""
        values = rp.state_mean_by_category_reply(self.test_job_id, self.test_dict['question'][0],
                                            self.test_dict['state'][0], self.ingestor)
        d = DeepDiff(values, self.state_mean_by_cat_res, math_epsilon = 0.01)
        self.assertTrue(not d, "Failed state mean by category")
