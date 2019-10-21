from flask import Flask, request, render_template, abort, send_file, url_for
from redis import Redis
import pickle
from uuid import uuid4
from humanize import naturalsize
from datetime import datetime
import os

from download_token import DownloadToken

app = Flask(__name__, template_folder='views')
redis = Redis(host='localhost', port=6379, db=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/token', methods=['POST'])
def view_token():
    token_id = request.form.get('token')
    token = get_token(token_id)

    if token is None:
        return render_template('message.html', message = f'Der eingegebene Code "{token_id}" existiert nicht.')

    if not is_valid(token, request.remote_addr):
	    return render_template('message.html', message = f'Der eingegebene Code "{token_id}" ist abgelaufen.')

    # Create session key
    session = create_session(token.id)

    # Update file sizes
    for file in token.files:
        file['size'] = naturalsize(os.path.getsize(file['path']))

    return render_template('token.html', token = token, session = session)

@app.route('/download/<session>/<int:id>')
def download(session, id):
    # Get token from session cache
    token_id = redis.get(session)
    if token_id is None:
        abort(401)
    
    token = get_token(token_id)
    if token is None:
        abort(404)
    
    token.downloads.append({'ip': request.remote_addr, 'datetime': datetime.now()})
    store_token(token)

    return send_file(token.files[id]['path'], as_attachment=True)
    
def get_token(token_id):
	if token_id is None:
		return None

	serialized_token = redis.get(token_id)
	if serialized_token is None:
		return None

	return pickle.loads(serialized_token)

def store_token(token):
    redis.set(token.id, pickle.dumps(token))

def is_valid(token, remote_addr):
    if not token.downloads:
        return True

    first_download = min(map(lambda d: d['datetime'], token.downloads))
    known_ip = remote_addr in map(lambda d: d['ip'], token.downloads)    
    number_of_ips = len(set(map(lambda d: d['ip'], token.downloads)))

    print(first_download, known_ip, number_of_ips)

    if datetime.now() - first_download > token.grace_period:
        return False

    if not known_ip and number_of_ips > 1:
        return False

    return True

def create_session(token_id):
    session_id = str(uuid4())    
    redis.set(session_id, token_id)
    redis.expire(session_id, 15*60)
    return session_id
	

app.run(host='localhost', port=8080, debug=True)