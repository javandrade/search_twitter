#!/usr/bin/python
# -*- coding: utf-8 -*-
import oauth2
#import json
import urllib.parse
import elasticsearch
import logging
import datetime
import numbers
import time
from subprocess import Popen, PIPE


def patch_tweet(d):
    """A API do twitter retorna as datas num formato que o elasticsearch não consegue reconhecer,
        então precisamos parsear a data para um formato que o ES entende, essa função faz isso.
    """

    if 'created_at' in d:
        # twitter uses rfc822 style dates. elasticsearch uses iso dates.
        # we translate twitter dates into datetime instances (pyes will
        # convert datetime into the right iso format understood by ES).
        new_date = datetime.datetime(*rfc822.parsedate(d['created_at'])[:6])
        d['created_at'] = new_date

    count_is_number = isinstance(d['retweet_count'], numbers.Number)
    if 'retweet_count' in d and not count_is_number:
        # sometimes retweet_count is a string instead of a number (eg. "100+"),
        # here we transform it to a number (an attribute in ES cannot have
        # more than one type).
        d['retweet_count'] = int(d['retweet_count'].rstrip('+')) + 1

    return d

# configurando traces e logs
log_dir = "/var/log/elasticsearch/"
tracer = logging.getLogger('elasticsearch.trace')
tracer.setLevel(logging.WARN)
tracer.addHandler(logging.FileHandler(log_dir + 'trace.log'))
default_logger = logging.getLogger('Elasticsearch')
default_logger.setLevel(logging.WARN)
default_logger.addHandler(logging.FileHandler(log_dir + 'default.log'))

# Criando conexão ao elasticsearch
es = elasticsearch.Elasticsearch(["0.0.0.0:9200"])

consumer_key = 'l60GcHVTld0Gg9cKlyeOqBI04'
consumer_secret = 'cRXvWhrAUnnkJ4YUnpd2NrFNpGTGvcWEAJUbM6jPfiwIQr9Yg2'
access_token = '287979768-B1CUatpqN19UV270AwTLpG5DVh6hyWSizTisRSNz'
access_token_secret = 'PloXQeMcPcAu8QHHYfQvVE1jnHdG8dQvwLJUjvgsJDywT'
consumer = oauth2.Consumer(consumer_key, consumer_secret)
token = oauth2.Token(access_token, access_token_secret)
cliente = oauth2.Client(consumer, token)

#while True:
    #time.sleep(5)

lista = ['#openbanking','#apifirst','#devops','#cloudfirst','#microservices','#apigateway','#oauth','#swagger','#raml']
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
        id = s['entities']['user_mentions']
        print(id)

#For each item in the stream (tweet data), save it on the elastisearch
    for s in v['statuses']:
        try:
            # Saving the tweet on the ES
            es.index(
                index="tweets",
                doc_type="tweet",
                body="patch_tweet(item)"
            )
        except:
           #caso haja qualquer problema com o elasticsearch ele verifica o estado e reinicia se necessário
            check_es_status()
            es = elasticsearch.Elasticsearch(["0.0.0.0:9200"])
            print ("Getting back to tweet recording")
