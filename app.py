from flask import Flask, request, render_template, abort
from redis import Redis
import pickle
from download_token import DownloadToken

app = Flask(__name__, template_folder='views')
redis = Redis(host='localhost', port=6379)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    token_id = request.form.get('token')
    token = get_token(token_id)

    if token is None:
        return render_template('message.html', message = f'Der eingegebene Code "{token_id}" existiert nicht.')

    if not is_valid(token, request.remote_addr):
	    return render_template('message.html', message = f'Der eingegebene Code "{token_id}" ist abgelaufen.')

    return render_template('token.html', token = token)
    
def get_token(token_id):
	if token_id is None:
		return None

	serialized_token = redis.get(token_id)
	if serialized_token is None:
		return None

	return pickle.loads(serialized_token)

def is_valid(token, remote_addr):
    if not token.downloads:
        return True
    return False

    
	

app.run(host='localhost', port=8080, debug=True)