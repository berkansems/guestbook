# Define Docker Compose command
DOCKER_COMPOSE = docker-compose

# Run tests in the 'web' container
test:
	$(DOCKER_COMPOSE) run web python manage.py test

# Build Docker images
build:
	$(DOCKER_COMPOSE) build

# Start Docker services
up:
	$(DOCKER_COMPOSE) up

# Build and run the Docker Compose services
run:
	$(DOCKER_COMPOSE) up --build


# Stop Docker services
down:
	$(DOCKER_COMPOSE) down

# Run custom management commands
migrations:
	$(DOCKER_COMPOSE) run web python manage.py makemigrations

createsuperuser:
	$(DOCKER_COMPOSE) run web python manage.py createsuperuser
