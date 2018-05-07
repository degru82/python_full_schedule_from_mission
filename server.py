import missiondb as db

import logging
logger = logging.getLogger('root')
logging.basicConfig(level=logging.INFO)

from flask import Flask, request, send_from_directory, jsonify
app = Flask(__name__, static_url_path='')

@app.route('/')
def mission_requested():
    logger.debug('index page requested')
    return send_from_directory('.', 'webclient.html')

@app.route('/stoppoints')
def stoppoints_requested():
    stoppoints = []
    stoppoints = db.get_stoppoints() 
    return jsonify(stoppoints)

@app.route('/schedule')
def schedule_requested():
    fullSchedule = db.get_full_schedule()
    return jsonify(fullSchedule)

@app.route('/servicereq', methods=['POST'])
def riding_service_requesgted():
    servreq = request.json
    logger.debug(f'REQUESTED in JSON: {servreq}')

    svcReqId, fullSchedule = db.service_requested_as(servreq)

    return jsonify(fullSchedule)

if __name__ == "__main__":
    app.run(debug=True)