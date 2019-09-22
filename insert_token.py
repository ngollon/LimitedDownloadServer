from redis import Redis
import pickle
from download_token import DownloadToken

redis = Redis(host='localhost', port=6379, db=4)
token = DownloadToken("ASD", [{'path': 'app.py', 'description': 'Main File' }, { 'path':'.gitignore', 'description': 'Another file'}])

redis.set(token.id, pickle.dumps(token))