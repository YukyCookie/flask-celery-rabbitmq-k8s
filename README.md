# flask-celery-rabbitmq-k8s
## Import the image into Microk8s registry (building celery image as an example)
1. Build celery image
```
sudo docker build ./k8s-celerytwitter-hashtag/. -t celery-hashtag
```
2. Enable microk8s registry
```
sudo microk8s.enable registry
```
3. Save docker image to a tar file
```
sudo docker save celery-hashtag > celery-hashtag.tar
```
4. Import image into k8s registry with the default namespace - k8s.io
```
sudo microk8s ctr -n k8s.io image import celery-hashtag.tar
```
5. Verify the import by listing images. 
```
sudo microk8s ctr -n k8s.io images ls name~=celery
```
6. In the list of images, we could read the size of image, if the size of image is not normal, we could delete the image and reimport.
```
microk8s ctr images rm $(microk8s ctr images ls name~='celery' | awk {'print $1'})
```
7. Remove all the docker images as needed (optional)
```
docker rmi $(docker images -q) -f
```
Now the image on Microk8s is ready to use in the deployment.
