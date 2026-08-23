# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This is a **learning project** following the Django Roadmap 2026 (Junior → Middle Backend Developer).

**Фаза 2 — DRF + API: ✅ COMPLETE (2026-07-06)**
**Pre-Фаза 3 reinforcement: ✅ COMPLETE (2026-07-06) — ready to start Docker/Deploy**
**Project: E-commerce Product API** — Products, Categories, Reviews, Orders, OrderItems, Wishlist

Roadmap: `/Users/djoni1vincent/djoni/Obsidian-notes/100 Programming/Django Roadmap 2026.md`
Progress: `/Users/djoni1vincent/djoni/Obsidian-notes/100 Programming/progress.md`

### Phase 2 — all topics done
- [x] Serializers — `ModelSerializer`, nested serializers, custom validation
- [x] JWT Authentication — `djangorestframework-simplejwt`, access/refresh tokens
- [x] Generic Views + ViewSets + Router
- [x] Permissions — `IsAuthenticated`, custom `IsOwnerOrReadOnly`
- [x] Filtering + Search + Ordering — `django-filter`, `SearchFilter`, pagination
- [x] API Testing — `APITestCase`
- [x] Swagger / OpenAPI — `drf-spectacular`
- [x] Throttling, API Versioning (`/api/v1/`), `django-silk` profiling

### Pre-phase 3 TODO — all done (2026-07-06)

- [x] **Verify real test coverage.** Measured with `coverage` — 86%, above the 70% target.
- [x] **Build one small resource from scratch, unaided.** Built the `wishlist` app (own Django app, `OneToOneField` user ↔ `ManyToManyField` products, custom `add_product` action, ownership-isolated `get_queryset`, tests) with hints only, no code handed over.
- [x] **Move secrets out of `config/settings.py`.** `SECRET_KEY`/`DEBUG` now come from `.env` via `django-environ`; `.env` gitignored, `.env.example` committed as template.
- [x] **Remove `django-rest-swagger` from `pyproject.toml`.** Done.
- [x] **Push a clean commit + README pass.** README documents wishlist endpoints and `.env` setup; `pyrightconfig.json` committed intentionally; history split into logical commits.

**Approach:** go deep on fewer topics rather than covering everything shallowly. Understanding > speed.

**Next up: Фаза 3 — Docker + Deploy + AWS.** See roadmap for topic breakdown (Docker/docker-compose, Render/Railway deploy, AWS S3, GitHub Actions CI/CD, Sentry).

---

## Teaching mode (IMPORTANT — read before every session)

This developer is a beginner learning Django. Adapt all responses accordingly:

- **Never write the solution first.** Ask "what have you tried?" or "what do you think should happen here?" before helping.
- **Use hints, not answers.** If stuck after 2-3 attempts, give the minimal hint needed — not the full implementation.
- **Explain the WHY.** When pointing out an issue or suggesting an approach, always explain why, not just what.
- **After explaining anything**, ask the developer to explain it back in their own words or apply it in a small example.
- **Respond in Ukrainian** unless the developer writes in English.

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
uv run python manage.py test products         # run tests for one app
uv run python manage.py createsuperuser    # create admin user
```

## Architecture

Django project with settings in `config/` (not a same-named app directory):

- `config/` — project settings, root URLs, wsgi/asgi
- `products/` — products app (models, views, tests)
- `users/` — users app (models, views, tests)
- `wishlist/` — per-user wishlist app (models, serializers, views, tests)

**Settings module:** `config.settings`

## Installed packages

All of these are wired into `INSTALLED_APPS`/`MIDDLEWARE` in `config/settings.py`: `rest_framework`, `debug_toolbar`, `drf_spectacular`, `django_filters`, `silk`, `wishlist`. `django-stubs` is for mypy type checking only, not in `INSTALLED_APPS`. `django-environ` loads `SECRET_KEY`/`DEBUG` from `.env` (see `.env.example`).

## DRF conventions to follow

When building API endpoints, use:
- Serializers in `<app>/serializers.py`
- App-level URLs in `<app>/urls.py`, included from `config/urls.py`
- Class-based views (`APIView`, `ModelViewSet`, or generic views) over function-based views
