# Makefile

API1_IMAGE=ai25-quiz-api1
API2_IMAGE=ai25-quiz-api2

build-image:
	docker build -t $(API1_IMAGE) api1/.
	docker build -t $(API2_IMAGE) api2/.

# run-api1:
#	docker run -v "$(pwd)"/logs:/logs --rm -it ai25-quiz-api1 sh

# run-api2:
#	docker run -v "$(pwd)"/logs:/logs --rm -it ai25-quiz-api2 sh

