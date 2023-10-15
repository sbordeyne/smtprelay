IMAGE_NAME=sbordeyne/smtprelay
IMAGE_TAG=1.2.0

all:
	docker build --platform=linux/amd64 -t $(IMAGE_NAME):$(IMAGE_TAG) .
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(IMAGE_NAME):latest
	docker push $(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(IMAGE_NAME):latest
