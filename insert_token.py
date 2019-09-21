from redis import Redis
import pickle
from download_token import DownloadToken

redis = Redis(host='localhost', port=6379)
token = DownloadToken("ASD", ["/boo", "/yah"])

redis.set(token.id, pickle.dumps(token))