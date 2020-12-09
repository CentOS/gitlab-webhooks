SHELL = /bin/bash
REG = quay.io
ORG = lrossett
NAME = kernel-webhooks
TAG = latest

.PHONY: image/build
image/build:
	docker build -t ${REG}/${ORG}/${NAME}:${TAG} .


.PHONY: image/build/no-cache
image/build/no-cache:
	docker build --no-cache -t ${REG}/${ORG}/${NAME}:${TAG} .

.PHONY: image/push
image/push:
	docker push ${REG}/${ORG}/${NAME}:${TAG}
