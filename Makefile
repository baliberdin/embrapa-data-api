IMAGE_NAME=fiap-api
PORT=8000

build:
	@docker build -t ${IMAGE_NAME} .

run: build
	@docker run --rm -it --name ${IMAGE_NAME} -p ${PORT}:8000 ${IMAGE_NAME}

test: build
	@docker run --rm -it --name ${IMAGE_NAME} -p ${PORT}:8000 --entrypoint pytest ${IMAGE_NAME}