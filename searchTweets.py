import json
import oauth2
import urllib.parse
import time
from flask import Flask
from redis import Redis
import os


consumer_key = 'l60GcHVTld0Gg9cKlyeOqBI04'
consumer_secret = 'cRXvWhrAUnnkJ4YUnpd2NrFNpGTGvcWEAJUbM6jPfiwIQr9Yg2'
access_token = '287979768-B1CUatpqN19UV270AwTLpG5DVh6hyWSizTisRSNz'
access_token_secret = 'PloXQeMcPcAu8QHHYfQvVE1jnHdG8dQvwLJUjvgsJDywT'
consumer = oauth2.Consumer(consumer_key, consumer_secret)
token = oauth2.Token(access_token, access_token_secret)
cliente = oauth2.Client(consumer, token)

lista = ['#openbanking','#apifirst','#devops','#cloudfirst','#microservices','#apigateway','#oauth','#swagger','#raml','#openapis']
lista_result = []
for value in lista:
    query = (value)
    query_codificada = urllib.parse.quote(query, safe='')
    requisicao = cliente.request(f'https://api.twitter.com/1.1/search/tweets.json?q={query_codificada}')
    decodificar = requisicao[1].decode()
    objeto = json.loads(decodificar)
    lista_result.append(objeto)

for v in lista_result:
    for s in v['statuses']:
        #id = s['user']['screen_name']
        #id = s['user']['followers_count']
        id = s['entities']['user_mentions']
        #id =s['text']
        print(id)
host_redis = os.environ.get('HOST_REDIS', 'redis')
port_redis = os.environ.get('PORT_REDIS', 6379)

app = Flask(__name__)
redis = Redis(host=host_redis, port=port_redis)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'Hello World! %s times' % redis.get('hits')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
