"""Use pandas for reading from csv"""
import pandas

class DataIngestor:
    """Stores type of question and reads csv data using pandas"""
    def __init__(self, csv_path: str):

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time daily',
            'Ce faci'
        ]

        self.questions_best_is_max = [
            """Percent of adults who achieve at least 150 minutes a week of moderate-intensity 
            aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic activity 
            (or an equivalent combination)""",
            """Percent of adults who achieve at least 150 minutes a week of moderate-intensity 
            aerobic physical activity or 75 minutes a week of vigorous-intensity aerobic physical 
            activity and engage in muscle-strengthening activities on 2 or more days a week""",
            """Percent of adults who achieve at least 300 minutes a week of moderate-intensity
             aerobic physical activity or 150 minutes a week of vigorous-intensity aerobic 
             activity (or an equivalent combination)""",
            """Percent of adults who engage in muscle-strengthening activities on 2 or 
            more days a week""",
        ]

        self.data = pandas.read_csv(csv_path)

        # In order to reduce the execution time, I will keep the information necessary
        # for the questions in two dicts of dicts, in this way I will not iterate
        # through a set of 20k lines of information

        #     Structure of ordered_info: {"Question": {"State": [values]}}
        #     Structure of category: {"Question": {"State": {"StratCat1": {"Strat1": [values]}}}}
        self.ordered_info = {}
        self.category = {}

        row_count = len(self.data)

        for i in range(row_count):
            question = self.data["Question"][i]
            state = self.data["LocationDesc"][i]
            value = self.data["Data_Value"][i]

            if question in self.ordered_info:
                if state not in self.ordered_info[question]:
                    self.ordered_info[question][state] = []
            elif question not in self.ordered_info:
                self.ordered_info[question] = {}
                if state not in self.ordered_info[question]:
                    self.ordered_info[question][state] = []

            self.ordered_info[question][state].append(value)

        for i in range(row_count):
            question = self.data["Question"][i]
            state = self.data["LocationDesc"][i]
            value = self.data["Data_Value"][i]
            strat_cat1 = self.data["StratificationCategory1"][i]
            strat1 = self.data["Stratification1"][i]

            # Check for NaN
            if pandas.isna(strat1) or pandas.isna(strat_cat1):
                continue

            if question in self.category:
                if state in self.category[question]:
                    if strat_cat1 in self.category[question][state]:
                        if strat1 not in self.category[question][state][strat_cat1]:
                            self.category[question][state][strat_cat1][strat1] = []
                    else:
                        aux_dict = {}
                        aux_dict[strat1] = []
                        self.category[question][state][strat_cat1] = aux_dict
                else:
                    aux_dict, aux_dict2 = {}, {}
                    aux_dict[strat1] = []
                    aux_dict2[strat_cat1] = aux_dict
                    self.category[question][state] = aux_dict2
            else:
                aux_dict, aux_dict2, aux_dict3 = {}, {}, {}
                aux_dict[strat1] = []
                aux_dict2[strat_cat1] = aux_dict
                aux_dict3[state] = aux_dict2
                self.category[question] = aux_dict3

            self.category[question][state][strat_cat1][strat1].append(value)
