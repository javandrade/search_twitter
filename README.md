Aplicação para consulta de Hashtagś do Tweeter e envio para o ElasticSearch

docker-compose da raiz do projeto já possui as configurações para baixar o ElasticSearch e Grafana, enquanto a aplicação encontra-se no Docker Hub.
docker push javandrade/apptweets:searchtweet

Para fazer uso do ElasticSeach Docker necessário ajustar o "tweets.py" para enviar os dados para o mesmo, caso contrario o envio será para local.
