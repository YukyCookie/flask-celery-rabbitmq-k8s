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
CONSUMER_API_KEY = "YwGDiTisCDoZvD7RtpIJuSiBG"
CONSUMER_API_SECRET = "gYXChLk5Hq1OaWZvqg15almu458DJyqhKVvek8NaNd2WaOrZLD"
ACCESS_TOKEN = "1597522454318120961-q4bIdAvJzGfnVqiHjv4Cw6MxQT9qj8"
ACCESS_TOKEN_SECRET = "f3kUqA5RRJO0lzXLK6maI2CZ0TWrYKcwwKAfbWF3EhaqN"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAACq9kAEAAAAAPv1Re47n%2BL3Wo%2FLtVfqE2wJ4opA%3DH6S549Mz1T9s9OgACmZHkLaoffQVE87a8XUqc9MFaLZIncdUI7"

# CELERY CONFIGURATION

CELERY_BROKER_URL = "amqp://{}:{}@{}:{}".format(rabbitmq_user, rabbitmq_password, rabbitmq_server, rabbitmq_port)
CELERY_RESULT_BACKEND = "mongodb://{}:{}@{}:{}/twitter_db".format(mongo_user, mongo_password, mongo_server, mongo_port)

celery_hash = Celery("hashtag_module", broker = CELERY_BROKER_URL, backend = CELERY_RESULT_BACKEND)
celery_loc = Celery("loc_module", broker = CELERY_BROKER_URL, backend = CELERY_RESULT_BACKEND)
