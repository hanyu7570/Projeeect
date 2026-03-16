# GSInspect

This project is a centralized web-based system designed to manage and visualize ground support and rockbolt testing data. It allows engineers to query test results across different bolt products, filter by specific parameters, and overlay force-displacement curves to compare performances.

# How to run the backend

To run the backend, ensure that you have both Docker and Docker Compose installed and working.

You can check the two of them with the following commands:

```
docker --version
docker compose version
```

After that, you need to create `.env` file in `backend/web` folder. You can use `.env_example` as an example of the file structure.

Then just run docker and you are good to go

```
docker compose up --build
```

Some useful commands:
```
# Run in background
docker compose up --build -d

# Follow logs
docker compose logs -f web

# Open a shell in the container
docker compose exec web sh
docker compose exec db sh

# Run Django management commands
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Tear everything down including the database volume
docker compose down -v
```