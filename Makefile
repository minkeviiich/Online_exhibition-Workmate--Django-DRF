DOCKER_COMPOSE = docker-compose
PYTEST = pytest

# Запуск тестов с использованием 4 ядер
test:
	$(DOCKER_COMPOSE) run --rm app $(PYTEST) -n 4

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

build:
	$(DOCKER_COMPOSE) build