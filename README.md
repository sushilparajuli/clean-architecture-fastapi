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
Note: Adding a `.env` file to version control is generally considered bad practice. In this project, it is used for simplicity as there is no sensitive information. Please create a `.env` file in the root directory.

#### `.env` File Template
Create a `.env` file in the project root with the following variables:
```env
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_db_name
DB_PORT=5432
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

---
*Built with ❤️ using FastAPI*
