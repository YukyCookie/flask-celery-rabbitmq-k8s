import os
import pymongo
import base64
from celery import Celery
from kubernetes import client, config


# Configure K8s Client and read secrets
if 'KUBERNETES_SERVICE_HOST' in os.environ:
    kubernetes_service_host = os.environ['KUBERNETES_SERVICE_HOST']
    config.load_incluster_config()

else:
    config.load_kube_config('/var/snap/microk8s/current/credentials/client.config')

v1 = client.CoreV1Api()
# MONGODB
mongo_server = os.environ.get("MONGODB_SERVICE_SERVICE_HOST")
mongo_port = 27017
mongo_secret = v1.read_namespaced_secret("mongodb-secret", "twitter-website").data
mongo_user = base64.b64decode(mongo_secret["username"]).decode("utf-8")
mongo_password = base64.b64decode(mongo_secret["password"]).decode("utf-8")

# RABBITMQ
rabbitmq_server = os.environ.get("RABBITMQ_SERVICE_SERVICE_HOST")
rabbitmq_port = os.environ.get("RABBITMQ_SERVICE_SERVICE_PORT_AMQP")
rabbitmq_secret = v1.read_namespaced_secret("rabbitmq-secret", "twitter-website").data
rabbitmq_user = base64.b64decode(rabbitmq_secret["username"]).decode("utf-8")
rabbitmq_password = base64.b64decode(rabbitmq_secret["password"]).decode("utf-8")

# TWITTER CREDENTIALS
CONSUMER_API_KEY = "nPRZSo2EX61jiSQv6OJDI4pEP"
CONSUMER_API_SECRET = "UvJ7L57faQilBEc5XwSpUmzTwQjJe1PfvZmFaZEhNsk828OPpCD"
ACCESS_TOKEN = "1597522454318120961-FAplOSuHfjtHYE6fJj5w21l3WHLSi8"
ACCESS_TOKEN_SECRET = "5iJFdBaMxpb3UqMYQSdy7CVH74ydJz7IvEvpY3AjRy2aq"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACq9kAEAAAAA1JMM%2BGIFruCLJ5AncvYx9EEz4Us%3Da7KzNs1JtOIcMWZ6INa4hYC577dQcFIDPk2fMhnELaZXDdE4tT"

# CELERY CONFIGURATION

CELERY_BROKER_URL = "amqp://{}:{}@{}:{}".format(rabbitmq_user, rabbitmq_password, rabbitmq_server, rabbitmq_port)
CELERY_RESULT_BACKEND = "mongodb://{}:{}@{}:{}/twitter_db".format(mongo_user, mongo_password, mongo_server, mongo_port)

celery_app = Celery("hashtag_module.tasks", broker = CELERY_BROKER_URL, backend = CELERY_RESULT_BACKEND)

