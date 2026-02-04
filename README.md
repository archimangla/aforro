
# Aforro – Backend Developer Assignment

This repository contains the backend implementation for the **Aforro** assignment.  
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

## Project Setup and Run Instructions

### Prerequisites
- Docker  
- Docker Compose  

### Steps to Run

1. Clone the repository:
```bash
git clone <your-github-repo-url>
cd aforro
````

2. Build and start all services:

```bash
docker-compose up --build
```

3. Run database migrations:

```bash
docker-compose exec web python manage.py migrate
```

4. Access the application:

```
http://localhost:8000
```

To stop all services:

```bash
docker-compose down
```

---

## API Details

### Product Search API

**Endpoint**

```
GET /api/search/products/
```

**Query Parameters**

* `q` (string, optional) – keyword search
* `category` (string, optional)
* `min_price` (decimal, optional)
* `max_price` (decimal, optional)
* `store_id` (integer, optional)
* `in_stock` (true / false, optional)
* `sort` (`price` | `newest`, optional)
* `page` (integer, default = 1)
* `page_size` (integer, default = 10)

**Sample Response**

```json
{
  "page": 1,
  "page_size": 10,
  "total_results": 2,
  "results": [
    {
      "id": 1,
      "title": "Mouse",
      "price": "500.00",
      "category": "Electronics",
      "quantity": 8
    }
  ]
}
```

---

### Autocomplete Suggest API

**Endpoint**

```
GET /api/search/suggest/
```

**Query Parameters**

* `q` (string, required, minimum 3 characters)

**Rate Limiting**

* 20 requests per minute per IP (Redis-backed)

**Sample Response**

```json
["Keyboard", "Keypad"]
```

---

### Create Order API

**Endpoint**

```
POST /orders/
```

**Request Body**

```json
{
  "store_id": 1,
  "items": [
    {
      "product_id": 2,
      "quantity_requested": 1
    }
  ]
}
```

**Response**

```json
{
  "order_id": 5,
  "status": "CONFIRMED"
}
```

---

### Store Orders List API

**Endpoint**

```
GET /stores/{store_id}/orders/
```

**Sample Response**

```json
[
  {
    "id": 5,
    "status": "CONFIRMED",
    "total_items": 3,
    "created_at": "2026-02-04T10:00:00Z"
  }
]
```

---

## Assumptions and Design Decisions

* Docker and Docker Compose are used to ensure consistent and reproducible setup.
* PostgreSQL is used as the primary relational database.
* Redis is used as:

  * Celery message broker
  * Rate limiter for autocomplete API
* Celery handles asynchronous background tasks.
* Inventory updates during order creation are wrapped in database transactions to prevent race conditions.
* Authentication and authorization were not implemented as they were not required by the assignment scope.
* Focus was kept on backend API design, correctness, and scalability.

---

## Notes

* The application can be run entirely using Docker as described above.
* The repository contains complete backend source code as required.

