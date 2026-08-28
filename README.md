# User Management System

A robust user management application built with **FastAPI**, designed using **Clean Architecture** principles to ensure maintainability, scalability, and testability.

## 🏗️ Architecture

The project follows a clean architecture approach, organizing code into distinct layers:

- **Domain**: Contains core entities and business rules.
- **Application**: Implements use cases and services.
- **Infrastructure**: Handles database operations (SQLAlchemy), repositories, and external integrations.
- **Interface**: Defines API endpoints (FastAPI routers), dependencies, and request/response schemas.

## 🚀 Key Technologies

- **FastAPI**: High-performance web framework.
- **SQLAlchemy**: ORM for database interaction.
- **Alembic**: Database migration tool.
- **Pydantic**: Data validation and settings management.
- **Python 3.14+**

## ⚙️ Getting Started

### Prerequisites

- Python 3.14 or higher
- A running PostgreSQL database
- `uv` (recommended for dependency management)

## 🛠️ Using Makefile

For convenience, a `Makefile` is included to streamline common development tasks:

- `make setup`: Install dependencies.
- `make db-up`: Start the database container.
- `make db-down`: Stop the database container.
- `make run`: Start the development server.

### Environment Variables

Copy `.env.example` to create your local `.env` file:

```bash
cp .env.example .env
```

#### `.env` File Template

A `.env.example` file is provided in the repository root:

```env
DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/user_management_app"
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=user_management_app
DB_PORT=5432
DB_HOST=localhost
```

### Database Setup (Docker)

You can use the provided Docker Compose file to start a PostgreSQL instance. The configuration relies on the variables defined in your `.env` file.

To start the database:

```bash
docker-compose -f docker-compose-dev.yaml up -d
```

To stop the database:

```bash
docker-compose -f docker-compose-dev.yaml down
```

### Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd user-management
   ```

2. Install dependencies:
   ```bash
   make setup
   ```

### Running the Application

To start the development server:

```bash
make run
```

The API will be available at `http://127.0.0.1:8000`.

## 📂 Project Structure

The project follows **Clean Architecture**, organizing code into distinct layers to ensure maintainability:

- `app/core/`: Contains shared configuration, error handling, base database connection logic, and providers.
- `app/features/`: Contains feature-specific modules. Each feature is organized into:
  - `domain/`: Business logic, entities, and domain exceptions.
  - `application/`: Use cases, service interfaces, and service implementations.
  - `infrastructure/`: Database models, repositories, and data mappers.
  - `interface/`: API endpoints (FastAPI routers), dependencies, and schemas.
- `app/features/admin/country/`: An example feature module showcasing the clean architecture implementation.

## 📊 Adding a New Feature (End-to-End Architecture & Workflow)

When adding a new feature to the project, follow the Clean Architecture flow from start to end with full coverage across all layers.

### End-to-End Request & Data Flow Diagram

```mermaid
flowchart TD
    subgraph Client ["1. Client Layer"]
        REQ["HTTP Request: JSON / Params"]
        RES["HTTP Response: JSON"]
    end

    subgraph Interface ["2. Interface Layer (app/features/feature/interface)"]
        API["API Router: api.py"]
        SCH["Schemas / DTOs: schemas.py"]
        DEP["Dependency Injection: dependencies.py"]
    end

    subgraph Application ["3. Application Layer (app/features/feature/application)"]
        SVC["Application Service: feature_service.py"]
        IREPO["Repository Interface: feature_repository_interface.py"]
    end

    subgraph Domain ["4. Domain Layer (app/features/feature/domain)"]
        ENT["Domain Entity: feature_entity.py"]
        EXC["Domain Exceptions: exceptions.py"]
    end

    subgraph Infrastructure ["5. Infrastructure Layer (app/features/feature/infrastructure)"]
        MAP["Data Mappers: mappers/"]
        REPO["Repository Implementation: feature_repository.py"]
        MDL["SQLAlchemy Model: models/"]
    end

    subgraph Database ["6. Database & Persistence Layer"]
        DB[("PostgreSQL Database")]
        MIG["Alembic Migrations: alembic/"]
    end

    subgraph Tests ["7. Full Test Coverage (Unit & Integration)"]
        T_DOM["Unit Tests: Domain & Mappers"]
        T_SVC["Unit Tests: Application Services (Mock Repo)"]
        T_API["Integration Tests: API Endpoints (TestClient + DB)"]
    end

    %% Request Flow
    REQ -->|"1. HTTP Call"| API
    API -->|"2. Validate Request Body/Query"| SCH
    API -->|"3. Resolve Service via Depends"| DEP
    DEP -->|"Injects Repository & Session"| SVC
    SVC -->|"4. Business Rules & Validation"| ENT
    SVC -->|"5. Call Use Case Contract"| IREPO
    IREPO -.->|"Implemented By"| REPO
    REPO -->|"6. Convert Entity to Model"| MAP
    MAP -->|"7. Persist ORM Model"| MDL
    MDL -->|"8. Execute SQL Query"| DB

    %% Response Flow
    DB -->|"9. Raw Records"| MDL
    MDL -->|"10. Map Model to Entity"| MAP
    MAP -->|"11. Return Domain Entity"| REPO
    REPO -->|"12. Return Domain Result"| SVC
    SVC -->|"13. Return Entity / Result"| API
    API -->|"14. Serialize to Response Schema"| SCH
    SCH -->|"15. JSON Response"| RES

    %% Error Handling
    ENT -.->|"Raises"| EXC
    REPO -.->|"Raises"| EXC
    EXC -.->|"Handled by"| API

    %% Testing Relations
    T_DOM -.->|"Tests"| ENT
    T_DOM -.->|"Tests"| MAP
    T_SVC -.->|"Tests"| SVC
    T_API -.->|"Tests"| API
```

### Step-by-Step Implementation Guide

To implement a new feature with complete end-to-end coverage:

1. **Domain Layer (`app/features/<feature>/domain/`)**:
   - Define domain entities (`<feature>_entity.py`).
   - Define custom domain exceptions (`domain/exceptions/`).
2. **Application Layer (`app/features/<feature>/application/`)**:
   - Define repository interface/contract (`application/interface/i<feature>_repository.py`).
   - Implement application service/use cases (`application/<feature>_service.py`).
3. **Infrastructure Layer (`app/features/<feature>/infrastructure/`)**:
   - Define SQLAlchemy database model inheriting from `Base` (`infrastructure/models/<feature>_model.py`).
   - Create entity-to-model and model-to-entity mappers (`infrastructure/mappers/`).
   - Implement concrete repository conforming to the application interface (`infrastructure/repositories/<feature>_repository.py`).
4. **Interface Layer (`app/features/<feature>/interface/`)**:
   - Define request and response Pydantic schemas (`interface/schemas.py`).
   - Set up FastAPI dependency providers for database session, repository, and service (`interface/dependencies.py`).
   - Define API endpoints and routes (`interface/api.py`).
5. **Database Migration (`app/core/data/source/local/alembic/`)**:
   - Import the new model in Alembic's `env.py` (if not auto-imported).
   - Generate migration: `alembic revision --autogenerate -m "add_<feature>_table"`.
   - Apply migration: `alembic upgrade head`.
6. **Router Registration (`app/main.py`)**:
   - Export router in `app/features/<feature>/__init__.py`.
   - Register router in `app/main.py` using `app.include_router(...)`.
7. **Testing & Full Coverage**:
   - **Unit Tests**: Test domain entity rules and mapping functions.
   - **Service Tests**: Test application services using mocked repository interfaces.
   - **Integration / E2E Tests**: Test API endpoints using FastAPI `TestClient` with a test database session.

---

_Built with ❤️ using FastAPI_
