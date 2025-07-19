# Makefile

IMAGE_API1=ai25-quiz-api1
IMAGE_NAME=ai25-quiz-api2

build-image:
	docker build -t $(IMAGE_API1) api1/.
	docker build -t $(IMAGE_NAME) api2/.

