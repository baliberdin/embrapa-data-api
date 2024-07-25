IMAGE_NAME=embrapa-data-api
PORT=8000

build:
	@docker build --build-arg="IMAGE_NAME=${IMAGE_NAME}"  -t ${IMAGE_NAME} .

run: build
	@docker run --rm -it --name ${IMAGE_NAME} -p ${PORT}:8000 ${IMAGE_NAME}

run-bash: build
	@docker run --rm -it --name ${IMAGE_NAME} -p ${PORT}:8000 --entrypoint bash ${IMAGE_NAME}

test: build
	@docker run --rm -it --name ${IMAGE_NAME} -p ${PORT}:8000 --entrypoint /opt/${IMAGE_NAME}/bin/test.sh ${IMAGE_NAME}