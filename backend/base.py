from flask import Flask, jsonify, request
import requests
import time
from flask_cors import CORS
import schedule
import threading


api = Flask(__name__)
CORS(api)

inception_time = time.time()
delayed_lines = set()
delayed_line_started = {}
delayed_line_total_time = {}



# calls MTA Api to get current delayed lines and prints changes in delays to console
def get_line_delays():
    api_url = 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/camsys%2Fsubway-alerts.json'
    response = requests.get(api_url)
    response_json = response.json()

    prev_delayed_lines = delayed_lines.copy()
    delayed_lines.clear()

    for entity in response_json['entity']:
        alert = entity['alert']
        if alert['transit_realtime.mercury_alert']['alert_type'] == 'Delays':
            for line in alert['informed_entity']:
                if "route_id" in line:
                    delayed_lines.add(line["route_id"])

    for line in delayed_lines:
        if line not in prev_delayed_lines:
            print("Line %s is experiencing delays" % line)
            delayed_line_started[line] = time.time()

    for line in prev_delayed_lines:
        if line not in delayed_lines:
            print("Line %s is now recovered" % line)
            delayed_line_total_time[line] = time.time() - delayed_line_started[line]


# calculates uptime for given line, which is the fraction of time that it has not been delayed since inception
def calculate_uptime(line):
    if line not in delayed_line_started:    # if no delay
        return 1
    
    total_time = time.time() - inception_time
    total_time_delayed = 0

    if line in delayed_lines: # taking time from current delay
        total_time_delayed += time.time() - delayed_line_started[line]

    if line in delayed_line_total_time: # taking times from previous delays
        total_time_delayed += delayed_line_total_time[line]

    uptime = 1 - (total_time_delayed / total_time)
    return uptime


# line status endpoint
@api.route('/status', methods=['GET'])
def get_status():
    line = request.args.get('line_name')
    if line:
        if line in delayed_lines:
            return jsonify({'status': 'delayed'})
        else:
            return jsonify({'status': 'not delayed'})
    else:
        return jsonify({'error': 'Missing line_name parameter'}), 400

# line uptime endpoint
@api.route('/uptime', methods=['GET'])
def get_uptime():
    line = request.args.get('line_name')
    if line:
        uptime = calculate_uptime(line)
        return jsonify({'uptime': uptime})
    else:
        return jsonify({'error': 'Missing line_name parameter'}), 400
    

# monitors MTA every 2 seconds
schedule.every(2).seconds.do(get_line_delays)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    
    api.run()