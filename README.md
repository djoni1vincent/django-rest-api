# Django REST API — Product Catalog

A REST API for a product catalog with categories, reviews, and orders. Built with Django REST Framework, JWT authentication, and auto-generated OpenAPI docs via Swagger UI.

## Tech Stack

- Python 3.14 / Django 6
- Django REST Framework
- JWT auth — `djangorestframework-simplejwt`
- OpenAPI schema + Swagger UI — `drf-spectacular`
- Filtering / search / ordering — `django-filter`
- PostgreSQL

## Setup

```bash
git clone https://github.com/djoni1vincent/django-rest-api.git
cd django-rest-api
uv sync
cp .env.example .env  # fill in PostgreSQL credentials
uv run python manage.py migrate
uv run python manage.py runserver
```

Open `http://localhost:8000/` — redirects to Swagger UI.

## API Endpoints

| Method | Endpoint | Access |
|---|---|---|
| `GET` | `/api/products/` | Public |
| `POST` | `/api/products/` | Admin only |
| `GET` | `/api/products/{id}/` | Public |
| `PUT/PATCH/DELETE` | `/api/products/{id}/` | Admin only |
| `GET/POST` | `/api/categories/` | Public / Admin |
| `GET/POST` | `/api/reviews/` | Auth required |
| `PUT/DELETE` | `/api/reviews/{id}/` | Owner only |
| `POST` | `/api/token/` | — (get JWT) |
| `POST` | `/api/token/refresh/` | — |

## Key Implementation Details

- **Nested serializers** — `ProductSerializer` returns full `CategorySerializer` on read, accepts `category_ids` (list of PKs) on write
- **Custom permission** — `IsOwnerOrReadOnly`: allows safe methods for all, write only for the object's `author`
- **Custom user model** — `CustomUser` extends `AbstractUser`, uses email as `USERNAME_FIELD`, adds `role` field
- **Filtering** — products support filter by name, category, price range; search by name/category name; ordering by name/price

## What I'd improve next

- Add pagination to all list endpoints
- Wire up the `users/` endpoints (currently commented out)
- Add test coverage for permission edge cases
- Deploy with Docker Compose + PostgreSQL
