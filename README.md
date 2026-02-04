# Aforro – Backend Developer Assignment

This repository contains the backend implementation for the Aforro assignment.  
The project is built using **Django**, **Django REST Framework**, **PostgreSQL**, **Redis**, **Celery**, and **Docker**.

---

## Tech Stack

- Python 3.11
- Django 5.x
- Django REST Framework
- PostgreSQL
- Redis
- Celery
- Docker & Docker Compose

---

## Project Setup (Using Docker)

### Prerequisites
- Docker
- Docker Compose

---

### Steps to Run

1. Clone the repository:
git clone <your-github-repo-url>
cd aforro

2. Build and Start Services
docker-compose up --build

3. Run DB migrations
docker-compose exec web python manage.py migrate

4. 4. server will be available at:
http://localhost:8000

4. server will be available at:
http://localhost:8000
