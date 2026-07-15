# E-commerce Product API

A RESTful API for an e-commerce platform built with Django REST Framework, featuring JWT authentication, API versioning, request throttling, query performance profiling, S3-backed media storage, error tracking, and a Dockerized PostgreSQL/Redis stack.

**Live:** [django-rest-api-yljl.onrender.com](https://django-rest-api-yljl.onrender.com) — deployed on Render, redeployed automatically on every push to `master` via GitHub Actions.

## Features

- **JWT Authentication** — token-based auth via `djangorestframework-simplejwt`, with custom claims (username, email, role) embedded in the access token
- **Products, Categories & Reviews** — full CRUD via DRF ViewSets and routers
- **Custom Permissions** — read-only access for anonymous users, write access restricted to admins/owners (`IsAdminUser`, `IsOwnerOrReadOnly`)
- **Filtering, Search & Ordering** — `django-filter` for field-level filters (name, category, price), full-text search, and ordering
- **Pagination** — page-number based pagination
- **Rate Limiting** — global throttling for anonymous/authenticated users, plus a stricter scoped throttle on the login endpoint to mitigate brute-force attempts
- **API Versioning** — URL path versioning (`/api/v1/`, `/api/v2/`); v2 introduces a richer price representation (`{amount, currency}`) while v1 stays backward-compatible
- **OpenAPI Documentation** — interactive Swagger UI per API version, generated with `drf-spectacular`
- **Query Profiling** — `django-silk` integration for inspecting SQL queries and catching N+1 issues
- **Wishlist** — authenticated users can maintain a personal wishlist of products
- **AWS S3 Media Storage** — user-uploaded media served via `django-storages` + `boto3`; static files served separately via WhiteNoise
- **Error Tracking** — Sentry captures exceptions and logs in production (`DEBUG=False`); disabled locally/in tests so it never sends dev noise
- **CI/CD** — GitHub Actions pipeline: lint (`ruff`) → test (`manage.py test` against a real PostgreSQL service) → deploy (triggers a Render deploy hook) on every push to `master`

## Tech Stack

- [Django](https://www.djangoproject.com/) 6
- [Django REST Framework](https://www.django-rest-framework.org/)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/) — JWT authentication
- [django-filter](https://django-filter.readthedocs.io/) — filtering
- [drf-spectacular](https://drf-spectacular.readthedocs.io/) — OpenAPI schema & Swagger UI
- [django-silk](https://github.com/jazzband/django-silk) — request/query profiling
- [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/)
- [django-environ](https://django-environ.readthedocs.io/) — environment-based configuration
- [uv](https://docs.astral.sh/uv/) — dependency management and task running
- [PostgreSQL](https://www.postgresql.org/) — primary database
- [Redis](https://redis.io/) — provisioned as a Docker Compose service, not yet wired into the app (reserved for future caching/Celery work)
- [Docker](https://docs.docker.com/) & [Docker Compose](https://docs.docker.com/compose/) — containerized local development (Django + PostgreSQL + Redis)
- [django-storages](https://django-storages.readthedocs.io/) + [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) — AWS S3 media storage
- [sentry-sdk](https://docs.sentry.io/platforms/python/guides/django/) — error tracking and logging in production
- [GitHub Actions](https://docs.github.com/en/actions) — CI/CD pipeline
- [Render](https://render.com/) — hosting/deployment

## Getting Started

### Option A: Docker Compose (recommended)

Runs Django, PostgreSQL, and Redis together.

**Prerequisites:** [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)

```bash
git clone <repo-url>
cd django-rest-api
cp .env.example .env  # fill in SECRET_KEY, POSTGRES_*, AWS_* (S3 bucket), DSN (Sentry, only used when DEBUG=False)
docker-compose up --build
```

The `web` container waits for PostgreSQL to report healthy, then runs migrations automatically via `entrypoint.sh` before starting the dev server. Create a superuser in a separate shell once the containers are up:

```bash
docker-compose exec web uv run python manage.py createsuperuser
```

The API will be available at `http://127.0.0.1:8000/`.

### Option B: Local (uv + local PostgreSQL)

**Prerequisites:**

- Python 3.14+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A running local PostgreSQL instance

```bash
git clone <repo-url>
cd django-rest-api
uv sync
cp .env.example .env  # fill in SECRET_KEY, AWS_*, DSN; set DB_HOST=localhost (not "db") to reach your local PostgreSQL
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## API Overview

| Endpoint | Description |
|---|---|
| `POST /api/token/` | Obtain a JWT access/refresh token pair (rate-limited: 5/min) |
| `POST /api/token/refresh/` | Refresh an access token |
| `GET/POST /api/v1/products/` | List/create products (v1: flat `price`) |
| `GET/POST /api/v2/products/` | List/create products (v2: `price` as `{amount, currency}`) |
| `GET/POST /api/v1/categories/` | List/create categories |
| `GET/POST /api/v1/reviews/` | List/create product reviews |
| `GET /api/v1/wishlist/` | View the authenticated user's wishlist |
| `POST /api/v1/wishlist/add_product/` | Add a product to the authenticated user's wishlist |
| `/api/schema/v1/swagger-ui/` | Swagger UI — v1 |
| `/api/schema/v2/swagger-ui/` | Swagger UI — v2 |
| `/admin/` | Django admin |
| `/silk/` | Query profiling dashboard |

## Running Tests

```bash
uv run python manage.py test
```

## Project Structure

```
config/              # project settings, root URLs
products/            # products, categories, reviews — models, serializers, views, filters
users/               # custom user model, JWT serializer/view
wishlist/            # per-user wishlist — model, serializer, views
Dockerfile           # Django app image (uv-based)
docker-compose.yml   # web + db (PostgreSQL) + redis services
entrypoint.sh        # runs migrations, then starts the dev server
.github/workflows/   # CI/CD pipeline (lint → test → deploy)
```

## Planned Improvements

- Wire up Redis for caching / Celery task queue
- Nginx + Gunicorn reverse proxy (optional, currently deployed via Render's own proxy)
