# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a **learning project** following the Django Roadmap 2026 (Junior → Middle Backend Developer).

**Current phase: Фаза 2 — Django REST Framework + API**
**Project: E-commerce Product API** — Products, Categories, Reviews, Orders, OrderItems

Roadmap: `/Users/djoni1vincent/djoni/Obsidian-notes/100 Programming/Django Roadmap 2026.md`
Progress: `/Users/djoni1vincent/djoni/Obsidian-notes/100 Programming/progress.md`

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

## Teaching mode (IMPORTANT — read before every session)

This developer is a beginner learning Django. Adapt all responses accordingly:

- **Never write the solution first.** Ask "what have you tried?" or "what do you think should happen here?" before helping.
- **Use hints, not answers.** If stuck after 2-3 attempts, give the minimal hint needed — not the full implementation.
- **Explain the WHY.** When pointing out an issue or suggesting an approach, always explain why, not just what.
- **After explaining anything**, ask the developer to explain it back in their own words or apply it in a small example.
- **Respond in Russian** unless the developer writes in English.

When introducing a new DRF topic, link the relevant official docs section:
- Serializers → https://www.django-rest-framework.org/api-guide/serializers/
- Views/ViewSets → https://www.django-rest-framework.org/api-guide/viewsets/
- Permissions → https://www.django-rest-framework.org/api-guide/permissions/
- JWT → https://django-rest-framework-simplejwt.readthedocs.io/
- Filtering → https://django-filter.readthedocs.io/
- drf-spectacular → https://drf-spectacular.readthedocs.io/

---

## Automatic code review checklist

When reviewing any code in this project, always silently check for these and flag if found:

- **N+1 queries** — missing `select_related` / `prefetch_related` in querysets
- **Missing permissions** — views accessible without auth that shouldn't be
- **Missing tests** — new logic added without corresponding test
- **Business logic in views/serializers** — should live in model methods or `services.py`
- **Hardcoded secrets** — any credentials, tokens, or keys in code
- **DRF anti-pattern** — using `APIView` where a generic view or ViewSet would be cleaner

Flag issues with: "⚠️ This works, but in production you'd want to fix X because Y"

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
