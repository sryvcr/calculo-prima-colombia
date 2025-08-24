# Nombre y tag de la imagen de docker
IMAGE_NAME=prima-colombia
TAG=latest

# Si no se pasa JSON_FILE, usa employee_1.json como default
JSON_FILE ?= /app/samples/employee_1.json

# Construir la imagen
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Ejecutar con un JSON_FILE dinámico
run:
	docker run --rm --entrypoint python $(IMAGE_NAME):$(TAG) main.py $(JSON_FILE)

# Ejecutar tests
test:
	docker run --rm $(IMAGE_NAME):$(TAG) pytest -s -p no:warnings

# Ejecutar bash
bash:
	docker run --rm -it $(IMAGE_NAME):$(TAG) bash
