from flask import Flask
from flask import request

app = Flask(__name__)
# define a route which takes a POST request and returns a response
@app.route('/create', methods=['POST'])
def api():
    start = request.form.get('start')
    stop = request.form.get('stop')
    return 'Hello, World!'

#create route to stop generation
@app.route('/stop', methods=['POST'])
def stop():
    try:
        return 'Stopped'
    except:
        return 'Error stopping generation'