stack_up:
	docker compose --profile stack up --build -d --scale upserver-interface=0 --scale upserver-alerts=0 --scale upserver-monitoring=0     

stack_down:
	docker compose --profile stack down  

prod:
	docker compose -f docker-compose.yml -f docker-compose.prod.yml --profile all up --build -d

dev:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml --profile all up --build -d

test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml --profile all up --build -d