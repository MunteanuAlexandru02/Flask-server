"""Treat all the requests and return replies"""
import json
from app import webserver as ws
from app.prev_replies import REPLIES

def create_states_dict(question,  ingestor, asc = True):
    """
    Creates a dictionary of states and orderes it in ASCENDING or DESCENDING order
    based on asc argument
    """
    states_dictionary = {}

    if question not in ws.prev_runs:
        for state, values in ingestor.ordered_info[question].items():
            median_value = float(sum(values) / len(values))
            states_dictionary[state] = median_value

        aux_dict = {REPLIES.STATES_MEAN: states_dictionary}
        ws.prev_runs[question] = aux_dict
    else:
        states_dictionary = ws.prev_runs[question][REPLIES.STATES_MEAN]

    # Used for the best5 or worst5 requests, based on the question type
    if asc is True:
        states_dictionary = dict(sorted(states_dictionary.items(), key=lambda item: item[1]))
    else:
        states_dictionary = dict(sorted(states_dictionary.items(), key=lambda item: item[1],
                reverse = True))

    return states_dictionary

def writes_to_file(path, content):
    """Takes the content and writes it in the file at path"""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(content, file)

def states_mean_reply(job_id_counter, question, ingestor):
    """Function to compute the request"""
    states_dictionary = create_states_dict(question, ingestor)

    writes_to_file(f"./results/job_id_{job_id_counter}", states_dictionary)

    return states_dictionary

def state_mean_reply(job_id_counter, question, state, ingestor):
    """Compute the state mean request"""
    # Used a dictionary with only one entry for easier return
    state_dictionary = {}

    length = len(ingestor.ordered_info[question][state])
    state_dictionary[state] = float(sum(ingestor.ordered_info[question][state]) / length)

    writes_to_file(f"./results/job_id_{job_id_counter}", state_dictionary)

    return state_dictionary

def best5_reply(job_id_counter, question, ingestor):
    """Compute the first 5 best results based on question"""
    states_dictionary = {}

    if question in ingestor.questions_best_is_min:
        states_dictionary = create_states_dict(question, ingestor)
    else:
        states_dictionary = create_states_dict(question, ingestor, False)

    # Take the first 5 elements from the dict
    first_5_elem = {x: states_dictionary[x] for x in list(states_dictionary.keys())[:5]}

    writes_to_file(f"./results/job_id_{job_id_counter}", first_5_elem)

    return first_5_elem

def worst5_reply(job_id_counter, question, ingestor):
    """Compute the first 5 worst results based on question"""
    states_dictionary = {}

    # The code is nearly the same as the one for best5, but the sort is done in
    # opposite contexts
    if question in ingestor.questions_best_is_min:
        states_dictionary = create_states_dict(question, ingestor, False)
    else:
        states_dictionary = create_states_dict(question, ingestor)

    first_5_elem = {x: states_dictionary[x] for x in list(states_dictionary.keys())[:5]}

    writes_to_file(f"./results/job_id_{job_id_counter}", first_5_elem)

    return first_5_elem

def global_mean_reply(job_id_counter, question, ingestor, write_file = True):
    """Computes the global mean based on a question"""
    total_sum = 0
    length = 0

    for _, values in ingestor.ordered_info[question].items():
        total_sum += sum(values)
        length += len(values)

    global_mean_dict = {}
    global_mean_dict["global_mean"] = float(total_sum / length)

    if write_file is True:
        writes_to_file(f"./results/job_id_{job_id_counter}", global_mean_dict)

    return global_mean_dict

def diff_from_mean_reply(job_id_counter, question, ingestor):
    """Will compute the states_dictionary and use a map"""
    states_dictionary = create_states_dict(question, ingestor)
    global_mean_dictionary = global_mean_reply(None, question, ingestor, False)

    global_mean_value = global_mean_dictionary["global_mean"]

    # Compute the difference between global_mean and the normal result by usign map
    new_dict = dict(map(lambda x: (x[0], global_mean_value - x[1]),
                        states_dictionary.items()))

    writes_to_file(f"./results/job_id_{job_id_counter}", new_dict)

    return new_dict

def state_diff_from_mean_reply(job_id_counter, question, state, ingestor):
    """The same logic as the above function, but will compute only for one state"""
    global_mean_dict = global_mean_reply(None, question, ingestor, False)
    global_mean_value = global_mean_dict["global_mean"]
    list_values = ingestor.ordered_info[question][state]

    state_value = sum(list_values) / len(list_values)
    state_value = global_mean_value - state_value

    new_dict = {state: state_value}

    writes_to_file(f"./results/job_id_{job_id_counter}", new_dict)

    return new_dict

def mean_by_category_reply(job_id_counter, question, ingestor):
    """
    Will go through a dict-of-dict-of-dict to reduce the number of
    lines searched
    """
    states_dictionary = {}

    for state, strat in ingestor.category[question].items():
        for strat_cat, values in strat.items():
            for strat1, values_list in values.items():
                tuple_key = f"('{state}', '{strat_cat}', '{strat1}')"
                median = float(sum(values_list) / len(values_list))
                states_dictionary[tuple_key] = median

    writes_to_file(f"./results/job_id_{job_id_counter}", states_dictionary)

    return states_dictionary

def state_mean_by_category_reply(job_id_counter, question, state, ingestor):
    """Will go only through 2 dicts because of the state contraint"""
    state_dictionary = {}
    state_dictionary[state] = {}

    for strat_cat, values in ingestor.category[question][state].items():
        for strat1, values_list in values.items():
            tuple_key = f"('{strat_cat}', '{strat1}')"
            median = float(sum(values_list) / len(values_list))
            state_dictionary[state][tuple_key] = median

    writes_to_file(f"./results/job_id_{job_id_counter}", state_dictionary)

    return state_dictionary
