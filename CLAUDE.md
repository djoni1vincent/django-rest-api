# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a **learning project** following the Django Roadmap 2026 (Junior → Middle Backend Developer).

**Current phase: Фаза 2 — Django REST Framework + API**
**Project: E-commerce Product API** — Products, Categories, Reviews, Orders, OrderItems

Roadmap file: `/Users/djoni1vincent/djoni/Obsidian-notes/100 Programming/Django Roadmap 2026.md`

### Фаза 2 checklist (what to implement)
- [ ] Serializers — `ModelSerializer`, nested serializers, custom validation
- [ ] JWT Authentication — `djangorestframework-simplejwt`, access/refresh tokens
- [ ] Generic Views + ViewSets + Router
- [ ] Permissions — `IsAuthenticated`, custom `IsOwnerOrReadOnly`
- [ ] Filtering + Search + Ordering — `django-filter`, `SearchFilter`, pagination
- [ ] API Testing — `APITestCase`, >70% coverage
- [ ] Swagger / OpenAPI — `drf-spectacular`
- [ ] Throttling, API Versioning (`/api/v1/`)

**Approach:** go deep on fewer topics rather than covering everything shallowly. Understanding > speed.

---

## Package manager

This project uses **uv** (not pip). Always use `uv` to manage dependencies and run commands:

```bash
uv add <package>          # add dependency
uv run python manage.py   # run manage.py commands
uv run python -m pytest   # run tests
```

## Common commands

```bash
uv run python manage.py runserver          # start dev server
uv run python manage.py makemigrations     # create migrations
uv run python manage.py migrate            # apply migrations
uv run python manage.py test               # run all tests
uv run python manage.py test posts         # run tests for one app
uv run python manage.py createsuperuser    # create admin user
```

## Architecture

Django project with settings in `config/` (not a same-named app directory):

- `config/` — project settings, root URLs, wsgi/asgi
- `posts/` — posts app (models, views, tests)
- `users/` — users app (models, views, tests)

**Settings module:** `config.settings`

## Installed packages (not yet wired up)

These packages are in `pyproject.toml` but not yet added to `INSTALLED_APPS` in `config/settings.py`:

- `djangorestframework` → add `'rest_framework'` to `INSTALLED_APPS`
- `django-debug-toolbar` → add `'debug_toolbar'` to `INSTALLED_APPS` + middleware
- `django-stubs` → for mypy type checking only, not in `INSTALLED_APPS`

## DRF conventions to follow

When building API endpoints, use:
- Serializers in `<app>/serializers.py`
- App-level URLs in `<app>/urls.py`, included from `config/urls.py`
- Class-based views (`APIView`, `ModelViewSet`, or generic views) over function-based views
