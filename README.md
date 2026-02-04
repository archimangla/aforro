\# Aforro – Backend Assignment



Aforro is a backend service for a multi-store product marketplace.  

It implements product search, autocomplete with rate limiting, inventory-aware ordering, and asynchronous order processing.



---



\## Tech Stack



\- Python 3.11

\- Django 5 + Django REST Framework

\- PostgreSQL

\- Redis

\- Celery

\- Docker \& Docker Compose



---



\## Core Features



\- Product search with filtering

\- Autocomplete suggestions with Redis-based rate limiting

\- Atomic inventory checks and stock deduction during order creation

\- Store-wise order listing with aggregation

\- Asynchronous order confirmation using Celery

\- Fully Dockerized development environment



---



\## Project Structure



```text

aforro/

├── project/          # Django project configuration

├── products/         # Product \& category models

├── stores/           # Store \& inventory models

├── orders/           # Orders \& order items

├── search/           # Search \& autocomplete APIs

├── docker-compose.yml

├── Dockerfile

├── requirements.txt

└── README.md



