import json
from flask import Flask
import logging
app = Flask(__name__)

@app.route('/status')
def status():
  response = app.response_class(
          response=json.dumps({"result":"OK - healthy"}),
          status=200,
          mimetype='application/json'
  )
  return response

@app.route('/metrics')
def metrics():
  response = app.response_class(
          response=json.dumps({"status":"success","code":0,"data":{"UserCount":140,"UserCountActive":23}}),
          status=200,
          mimetype='application/json'
  )
  return response

 
@app.route("/")
def hello():
  # Logging a CUSTOM message 
  app.logger.info('Main request successfull')
  return "Hello World!"

if __name__ == "__main__":
  # Stream logs to a file, and set the default log level to DEBUG
  logging.basicConfig(filename='app.log',level=logging.INFO)
  app.run(host='0.0.0.0')