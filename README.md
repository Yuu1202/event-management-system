# Event Management System

Event Ticketing & Booking System built with FastAPI, Clean Architecture, and Domain-Driven Design.

## Tech Stack
- Python + FastAPI
- PostgreSQL
- SQLAlchemy + Alembic
- JWT Authentication

## How to Run

### 1. Clone & Setup
```bash
git clone <repo-url>
cd event-management-system
python -m venv venv
venv\Scripts\Activate.ps1  # Windows
pip install -r requirements.txt
```

### 2. Configure PostgreSQL
Copy `.env.example` to `.env` and fill in your database credentials.

### 3. Run Migration
```bash
alembic upgrade head
```

### 4. Run Tests
```bash
pytest tests/
```

### 5. Run App
```bash
uvicorn main:app --reload
```

## Architecture
- `app/domain/` — Aggregates, Entities, Value Objects, Domain Events
- `app/application/` — Commands, Queries, Handlers, Interfaces
- `app/infrastructure/` — DB, Repositories, External Services
- `app/presentation/` — REST API Controllers

## 🚀 Project Roadmap & Progress Tracking

This project follows the development timeline and milestones specified in the "Case Study - Event Management System.pdf".

### **Week 8: Project Structure**
- [ ] Initialize Clean Architecture folder structure (Domain, Application, Infrastructure, Presentation)
- [ ] Define initial business rules based on user stories and acceptance criteria
- [ ] Draft initial Domain Model
- [ ] Document initial Ubiquitous Language glossary

### **Week 9-10: Domain Layer & Unit Tests**
- [ ] Implement DDD tactical patterns: Aggregates, Entities, and Value Objects
- [ ] Implement Domain Services and Domain Events
- [ ] Define Repository Interfaces
- [ ] Write and pass Unit Tests for domain logic

### **Week 11: Application Layer**
- [ ] Implement Commands, Queries, and their respective Handlers
- [ ] Create Data Transfer Objects (DTOs)
- [ ] Define Application Service Interfaces for external system interactions

### **Week 12: Infrastructure Layer**
- [ ] Design PostgreSQL schema and migration files
- [ ] Implement Repository interfaces using PostgreSQL
- [ ] Implement Application Service implementations (Payment Gateway, Notifications, etc.)
- [ ] Configure database connections and environment settings

### **Week 13: Presentation Layer & Final Integration**
- [ ] Implement REST API Controllers
- [ ] Verify working endpoints with request/response examples
- [ ] Ensure full integration between Controller, Application, Infrastructure, and Database layers

---
*Note: Progress is updated weekly following the course milestones.*