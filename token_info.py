from redis import Redis
import pickle
from download_token import DownloadToken
import string
import sys

redis = Redis(host='localhost', port=6379, db=4)

token_id = sys.argv[1]

def get_token(token_id):
	if token_id is None:
		return None

	serialized_token = redis.get(token_id)
	if serialized_token is None:
		return None

	return pickle.loads(serialized_token)

token = get_token(token_id)
print(token.__dict__)
