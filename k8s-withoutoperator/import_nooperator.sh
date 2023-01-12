sudo docker build ./k8s-withoutoperator/flask/. -t flask
sudo docker save flask > flask.tar
sudo microk8s ctr -namespace k8s.io image import flask.tar

sudo docker build ./k8s-withoutoperator/celery-hashtag/. -t celery-hashtag
sudo docker save celery-hashtag > celery-hashtag.tar
sudo microk8s ctr -namespace k8s.io image import celery-hashtag.tar

sudo docker build ./k8s-withoutoperator/celery-loc/. -t celery-location
sudo docker save celery-hashtag > celery-location.tar
sudo microk8s ctr -namespace k8s.io image import celery-location.tar