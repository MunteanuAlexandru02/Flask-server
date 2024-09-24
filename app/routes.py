"""Treats the flask requests"""
from flask import request, jsonify
from app import webserver as ws
from app.replies import states_mean_reply, state_mean_reply, best5_reply, worst5_reply
from app.replies import global_mean_reply, diff_from_mean_reply, state_diff_from_mean_reply
from app.replies import mean_by_category_reply, state_mean_by_category_reply

def send_to_threadpool(function_name, need_state = False):
    """receive a function and call it with correct args"""
    data = request.json
    question = data["question"]

    ws.logger.info("Received request for %s and the data: %s", function_name, data)

    with ws.counter_lock:
        ws.job_counter += 1

    key = f"job_id_{ws.job_counter}"
    ws.logger.info("Created job for the previous request: %s", key)

    if need_state is True:
        state = data["state"]
        future = ws.tasks_runner.tp_executor.submit(function_name, ws.job_counter,
                                question, state, ws.data_ingestor)
    else:
        future = ws.tasks_runner.tp_executor.submit(function_name, ws.job_counter,
                                        question, ws.data_ingestor)

    with ws.job_lock:
        ws.job_dictionary[key] = future


    return key

# Example endpoint definition
@ws.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    """Function defined by ASC team. I did not touch it :P"""
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    # Method Not Allowed
    return jsonify({"error": "Method not allowed"}), 405

@ws.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    """Checks the validity of a job and returns info accordingly"""

    if job_id not in ws.job_dictionary:
        ws.logger.info("Job with the id: %s is not registered", job_id)
        return jsonify({'status': 'error', 'reason': 'Invalid job_id'})

    if ws.job_dictionary[job_id].done():
        ws.logger.info("Job with the id: %s is done", job_id)
        info = ws.job_dictionary[job_id].result()
        return jsonify({'status': 'done', 'data': info})

    ws.logger.info("Job with the id: %s is still running", job_id)
    return jsonify({'status': 'running'})

@ws.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """Will check if I will accept requests, if I can, will submit a new thread to TP"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(states_mean_reply)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """Compute the mean for only one state"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(state_mean_reply, True)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/best5', methods=['POST'])
def best5_request():
    """"Return the best 5 states based on the question"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(best5_reply)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/worst5', methods=['POST'])
def worst5_request():
    """"Return the worst 5 states based on the question"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(worst5_reply)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """Creates job for new global mean request and submits it to threadpool"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(global_mean_reply)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """Computes the difference between global mean and state mean for every state"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(diff_from_mean_reply)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """Computes the difference between global mean and state mean for only one state"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(state_diff_from_mean_reply, True)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """Computes the mean for every state and category"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(mean_by_category_reply)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)


@ws.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """Computes the mean for only one state and multiple categoriess"""
    if ws.running is False:
        ws.logger.info(ws.shut_down)
        return jsonify(ws.shut_down)

    key = send_to_threadpool(state_mean_by_category_reply, True)

    with ws.reply_lock:
        ws.reply_to_request['job_id'] = key
        ws.logger.info(ws.reply_to_request)

        return jsonify(ws.reply_to_request)

@ws.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown_request():
    """Shutdown task_runner and block future requests"""
    ws.tasks_runner.tp_executor.shutdown()
    ws.running = False

    ws.logger.info("Server is shutting down, should not be able to recv POST requests")
    return jsonify(ws.shutting_down)

@ws.route('/api/jobs', methods = ['GET'])
def jobs_request():
    """Return all the jobs and their state (done or running)"""
    job_dictionary = {}
    job_dictionary['status'] = 'done'
    job_dictionary['data'] = []
    aux_dict = {}

    ws.logger.info("jobs request received")
    with ws.job_lock:
        for key, value in ws.job_dictionary.items():
            if value.done() is True:
                aux_dict = {key: "done"}
            elif value.running() is True:
                aux_dict = {key, "running"}
            job_dictionary['data'].append(aux_dict)

    ws.logger.info("Output for jobs request: %s", job_dictionary)
    return jsonify(job_dictionary)

@ws.route('/api/num_jobs', methods = ['GET'])
def num_jobs_request():
    """"Count all the the running jobs"""
    counter = 0

    ws.logger.info("num_jobs request received")
    with ws.job_lock:
        for _, value in ws.job_dictionary.items():
            if value.running() is True:
                counter += 1

    ws.logger.info("Number of jobs that are still running: %d", counter)
    return jsonify({"status": "done", "num_jobs": counter})

# You can check localhost in your browser to see what this displays
@ws.route('/')
@ws.route('/index')
def index():
    """Flask function"""
    routes = get_defined_routes()
    msg = "Hello, World!\n Interact with the ws using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    """Flask function"""
    routes = []
    for rule in ws.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
