import os
import pymongo
import base64
from celery import Celery
from kubernetes import client, config
from kombu import Queue


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
CONSUMER_API_KEY = ""
CONSUMER_API_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
BEARER_TOKEN = ""


# CELERY CONFIGURATION

CELERY_BROKER_URL = "amqp://{}:{}@{}:{}".format(rabbitmq_user, rabbitmq_password, rabbitmq_server, rabbitmq_port)
CELERY_RESULT_BACKEND = "mongodb://{}:{}@{}:{}/twitter_db".format(mongo_user, mongo_password, mongo_server, mongo_port)

CELERY_QUEUES = (
    Queue('send_loc', routing_key='send.loc', queue_arguments={'x-max-priority': 1}),
    Queue('send_hash', routing_key='send.hash', queue_arguments={'x-max-priority': 1}),
    Queue('loc_queue', routing_key='loc.tasks', queue_arguments={'x-max-priority': 10}),
    Queue('hash_queue', routing_key='hash.tasks', queue_arguments={'x-max-priority': 10}),
)

CELERY_ROUTES=({
    'loc_module.tasks.search': {'queue': 'loc_queue', 'routing_key': 'loc.tasks',},
    'loc_module.tasks.insert_data': {'queue': 'send_loc', 'routing_key': 'send.loc'},
    'hashtag_module.tasks.search': {'queue': 'hash_queue', 'routing_key': 'hash.tasks',},
    'hashtag_module.tasks.insert_data': {'queue': 'send_hash', 'routing_key': 'send.hash'},
    },
)

celery_app = Celery("hashtag_module.tasks", broker = CELERY_BROKER_URL, backend = CELERY_RESULT_BACKEND)

