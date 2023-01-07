
sudo docker build ./k8s-withoutoperator/flask/. -t flask
sudo docker save flask > flask.tar
sudo microk8s ctr -namespace k8s.io image import flask.tar

sudo docker build ./k8s-withoutoperator/celery-hashtag/. -t celery-hashtag
sudo docker save celery-hashtag > celery-hashtag.tar
sudo microk8s ctr -namespace k8s.io image import celery-hashtag.tar

sudo docker build ./k8s-withoutoperator/celery-loc/. -t celery-location
sudo docker save celery-hashtag > celery-location.tar
sudo microk8s ctr -namespace k8s.io image import celery-location.tar

---------------------------------------------------------------------------

sudo docker build ./k8s-withoperator/flask/. -t flask-oper
sudo docker save flask-oper > flask-oper.tar
sudo microk8s ctr -namespace k8s.io image import flask-oper.tar

sudo docker build ./k8s-withoperator/celery-hashtag/. -t celery-hashtag-oper
sudo docker save celery-hashtag-oper > celery-hashtag-oper.tar
sudo microk8s ctr -namespace k8s.io image import celery-hashtag-oper.tar

sudo docker build ./k8s-withoperator/celery-loc/. -t celery-location-oper
sudo docker save celery-location-oper > celery-location-oper.tar
sudo microk8s ctr -namespace k8s.io image import celery-location-oper.tar