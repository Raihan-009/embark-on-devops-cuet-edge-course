network:
	docker network create myapp-network

mysql:
	docker build -t mysql-app -f Dockerfile.mysql .
	docker run -d \
		--name mysql-container \
		--network myapp-network \
		-p 3306:3306 \
		mysql-app
	@echo "Waiting for MySQL to start..."
	@sleep 30

redis:
	docker build -t redis-app -f Dockerfile.redis .
	docker run -d \
		--name redis-container \
		--network myapp-network \
		-p 6379:6379 \
		redis-app
	@echo "Waiting for Redis to start..."
	@sleep 5

backend:
	docker build -t backend-app -f Dockerfile.backend .
	docker run -d \
		--name backend-container \
		--network myapp-network \
		-p 8000:8000 \
		backend-app
	@echo "Backend started at http://localhost:8000"

logs:
	@echo "MySQL logs:"
	@docker logs mysql-container
	@echo "\nRedis logs:"
	@docker logs redis-container
	@echo "\nBackend logs:"
	@docker logs backend-container

clean:
	docker stop mysql-container redis-container backend-container || true
	docker rm mysql-container redis-container backend-container || true
	docker network rm myapp-network || true

all: network mysql redis backend