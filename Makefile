make prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up --build -d

make dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up  up --build -d

make test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml up  up --build -d