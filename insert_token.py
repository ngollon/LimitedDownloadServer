from redis import Redis
import pickle
from download_token import DownloadToken
import string
import random
import sys

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

redis = Redis(host='localhost', port=6379, db=4)

tokenId = id_generator(4, "23456789") + "-" + id_generator(4, "23456789")

files = []

i = 1
while i < len(sys.argv):
    path = sys.argv[i]
    description = sys.argv[i + 1]
    file = {'path': path , 'description': description }
    files.append(file)
    i += 2

token = DownloadToken(tokenId, files)
print(f"Created token with ID {tokenId}. Contents: {str(files)}")

redis.set(token.id, pickle.dumps(token))