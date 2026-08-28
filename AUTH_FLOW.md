# Task: Add JWT + bcrypt Auth Flow (Clean Architecture) & Protect Country Mutations for Admin

## Context
- **Stack**: FastAPI, SQLAlchemy, Pydantic v2, Alembic, pytest, psycopg2
- **Architecture**: Clean Architecture (Layered / Feature-based)
- **Directory Layout**:
  ```
  app/
    core/              # config, database providers, shared exceptions, base models
    features/
      auth/            # Auth feature (domain, application, infrastructure, interface)
      admin/country/   # Existing country feature (domain, application, infrastructure, interface)
  ```
- **Requirements**:
  - Implement full JWT (access + refresh) + bcrypt authentication.
  - Protect Country mutation endpoints (`POST`, `PUT`, `PATCH`, `DELETE`) with admin role check.
  - Record audit logs for country mutations.

---

## Clean Architecture Constraints
| Layer | Dependencies | Contents |
|---|---|---|
| **domain** | None (pure Python) | Entities (`User`, `AuditLog`), Repository interfaces, Domain exceptions |
| **application** | domain | Services / Use cases (`AuthService`, `CountryService`), DTOs, interface ports |
| **infrastructure** | domain, application | SQLAlchemy models, Repository implementations, Password hasher, JWT service, Mappers |
| **interface** | application, core | FastAPI routers, Request/Response schemas, Dependencies (`get_current_user`, `require_admin`) |

*Rules*:
- No ORM or web framework dependencies in Domain and Application layers.
- Routers handle only HTTP serialization and call application services.

---

## Functional Requirements

### 1. User & Auth
- **User Entity**: `id`, `email` (unique), `hashed_password`, `role` (`admin` | `user`), `is_active`, `created_at`, `updated_at`.
- **Register (`POST /api/v1/auth/register`)**: Validate email/password, hash with bcrypt, store user, return created user (without password hash).
- **Login (`POST /api/v1/auth/login`)**: Validate credentials, return access and refresh JWT tokens.
- **Refresh (`POST /api/v1/auth/refresh`)**: Accept valid refresh token, issue new token pair.
- **Current User (`GET /api/v1/auth/me`)**: Require valid Bearer token, return current user profile.
- **Security**: Configurable bcrypt rounds; JWT claims (`sub`, `role`, `exp`, `iat`, `type`).

### 2. Country Authorization & Auditing
- `POST/PUT/PATCH/DELETE` country endpoints require `Authorization: Bearer <token>` + `role == admin` + `is_active == True`.
- Return `401 Unauthorized` if unauthenticated/token invalid; `403 Forbidden` if role is not admin.
- `GET` country endpoints remain public.
- Record an **Audit Log** upon successful country mutations (`user_id`, `action`, `resource_type`, `resource_id`, `metadata`, `created_at`).

---

## Implementation Blueprint

### Domain Layer (`app/features/auth/domain/` & `app/features/admin/country/domain/`)
- `auth/domain/user_entity.py`
- `auth/domain/audit_log_entity.py`
- `auth/domain/exceptions/auth_exception.py`
- `auth/domain/interface/iuser_repository.py`
- `auth/domain/interface/iaudit_log_repository.py`

### Application Layer (`app/features/auth/application/`)
- `auth/application/auth_service.py` (registration, login, refresh, get_current_user)
- Update `admin/country/application/country_service.py` to write audit logs and accept actor context.

### Infrastructure Layer (`app/features/auth/infrastructure/`)
- SQLAlchemy Models: `user_model.py`, `audit_log_model.py`
- Mappers: Entity <-> Model
- Repositories: `user_repository.py`, `audit_log_repository.py`
- Security Ports / Helpers: `bcrypt_hasher.py`, `jwt_service.py`
- Database migrations for `users` and `audit_logs` tables.

### Interface Layer (`app/features/auth/interface/`)
- Schemas: `schemas.py` (Register, Login, Token, UserResponse)
- Dependencies: `dependencies.py` (`get_current_user`, `require_admin`)
- Routers: `api.py` (`/api/v1/auth/*`)
- Update `admin/country/interface/api.py` with `Depends(require_admin)`.

---

## API Specification

```
POST /api/v1/auth/register  -> 201 Created (User info)
POST /api/v1/auth/login     -> 200 OK (access_token, refresh_token, token_type)
POST /api/v1/auth/refresh   -> 200 OK (access_token, refresh_token, token_type)
GET  /api/v1/auth/me        -> 200 OK (User info)

POST   /api/v1/admin/country/       [Admin Bearer Auth] -> 201 Created + Audit Log
PUT    /api/v1/admin/country/{id}   [Admin Bearer Auth] -> 200 OK + Audit Log
DELETE /api/v1/admin/country/{id}   [Admin Bearer Auth] -> 200 OK / 204 + Audit Log
GET    /api/v1/admin/country/       [Public]            -> 200 OK
GET    /api/v1/admin/country/{id}   [Public]            -> 200 OK
```

---

## Definition of Done
- [ ] Clean Architecture boundaries maintained without cross-layer leaks.
- [ ] Authentication endpoints functional (Register, Login, Refresh, Me).
- [ ] Role-based access control protecting country mutations (`admin` only).
- [ ] Audit logs captured for country create/update/delete operations.
- [ ] Alembic migrations generated and applied.
- [ ] Unit and integration tests covering auth flows and access control.
- [ ] Environment variables documented in `.env.example`.