build:
	docker compose -f docker-compose.yml build

up: build
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down