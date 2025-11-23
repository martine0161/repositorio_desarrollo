IMAGE_NAME := ejemplo-microservice
VERSION := 0.1.0
CONTAINER_NAME := ejemplo-ms

.PHONY: build run stop logs clean test

build:
	docker build --no-cache -t $(IMAGE_NAME):$(VERSION) .

run:
	docker run --rm -d --name $(CONTAINER_NAME) -p 80:80 $(IMAGE_NAME):$(VERSION)

stop:
	docker rm -f $(CONTAINER_NAME) || true

logs:
	docker logs -n 200 $(CONTAINER_NAME)

clean: stop
	docker image prune -f

test:
	pytest -q