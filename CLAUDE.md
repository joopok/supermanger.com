# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SuperManager is a Flask-based REST API backend for a freelancer management system. It provides comprehensive CRUD operations for managing freelancer profiles, skills, and related metadata with MySQL/MariaDB persistence.

**Tech Stack**: Flask 3.0.0, SQLAlchemy 3.1.1, Marshmallow 3.20.1, PyMySQL, MySQL/MariaDB

## Architecture & Code Organization

### Layered Architecture Pattern

The codebase follows a **4-layer architecture** for separation of concerns:

1. **Routes Layer** (`app/routes/freelancer_routes.py`) - Request handling & HTTP validation
   - Blueprint-based route definitions
   - Query parameter extraction
   - Request/response serialization via schemas
   - Error handling via `handle_error`/`handle_success` utilities

2. **Schema Layer** (`app/schemas/freelancer_schema.py`) - Data validation & serialization
   - Marshmallow schemas for request validation (FreelancerCreateSchema, FreelancerUpdateSchema)
   - Response serialization (FreelancerSchema, SkillSchema)
   - Declarative field validation with custom validators

3. **Service Layer** (`app/services/freelancer_service.py`) - Business logic
   - Static methods for all operations (get_list, get_by_id, create, update, delete, get_skills)
   - Filtering, sorting, and pagination logic
   - Email uniqueness checks and error handling
   - Many-to-many skill relationship management

4. **Model Layer** (`app/models/freelancer.py`) - Data persistence
   - SQLAlchemy ORM models (Freelancer, Skill)
   - Association table (`freelancer_skill`) for many-to-many relationships
   - Utility methods: `to_dict()` for serialization
   - Timestamp fields: `created_at`, `updated_at`

**Key Pattern**: Routes → Schemas → Services → Models → Database

### Data Model Structure

**Freelancer** - UUID primary key, indexed on name/email for search optimization, JSON field for portfolio items, timestamps auto-managed

**Skill** - String ID primary key (e.g., "react", "nodejs"), belongs-to-many Freelancer via association table

**Many-to-Many Relationship**: `freelancer_skill` association table enables flexible skill management with cascade operations

### Application Factory & Configuration

- **app/__init__.py**: Flask application factory pattern with CORS setup, database initialization, route registration, error handlers
- **config.py**: Environment-based configuration (development/production/testing) with MySQL connection string from `.env`
- **Database URI**: `mysql+pymysql://{user}:{password}@{host}:{port}/{database}`

## Development Commands

### Setup & Database

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize skills (must run first)
python init_skills.py

# Initialize test data (optional, after skills)
python init_data.py
```

### Running the Server

```bash
# Development mode with debug enabled
python app.py

# Server runs on http://localhost:8000 by default
# API base: http://localhost:8000/api
```

### Testing & Health Checks

```bash
# Health check
curl http://localhost:8000/api/freelancers/health

# List freelancers with pagination
curl "http://localhost:8000/api/freelancers?page=1&limit=20"

# Get skills list
curl "http://localhost:8000/api/freelancers/skills"

# Get specific freelancer
curl "http://localhost:8000/api/freelancers/{freelancer_id}"
```

### Database Management

```bash
# MySQL connection from command line
mysql -h {DB_HOST} -u {DB_USER} -p

# Create database (one-time setup)
CREATE DATABASE supermanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## API Endpoints Reference

### Freelancer CRUD

- `GET /api/freelancers` - List with filters, sorting, pagination
- `GET /api/freelancers/{id}` - Get single freelancer
- `POST /api/freelancers` - Create freelancer
- `PUT /api/freelancers/{id}` - Update freelancer
- `DELETE /api/freelancers/{id}` - Delete freelancer

### Query Parameters for List Endpoint

- `page`, `limit` - Pagination (default: 1, 20)
- `search` - Search name/email/bio
- `skills` - Filter by skill IDs (array: `?skills=react&skills=nodejs`)
- `availability` - Filter by availability status
- `minRating`, `minExperience`, `maxHourlyRate` - Numeric filters
- `sortBy` - Sort field (name, rating, experience, hourlyRate, createdAt)
- `sortOrder` - asc or desc

### Skills

- `GET /api/freelancers/skills` - List all available skills

## Key Implementation Details

### Filtering & Query Building

The service layer builds queries incrementally:
```python
query = Freelancer.query
if search: query = query.filter(...)
if skills: query = query.join(Skill).filter(Skill.id.in_(skills)).distinct()
if availability: query = query.filter(...)
```

Use `.distinct()` when joining skills to avoid duplicates with many-to-many relationships.

### Pagination Utility

`app/utils.py:paginate()` returns dictionary with data, total, page, limit, totalPages - always used with query objects.

### Email Uniqueness

Enforced at service layer before create/update:
- Create: Check if email exists (raise ValueError)
- Update: Check if email exists AND belongs to different freelancer

### Skill Management

Skills are pre-loaded in database via `init_skills.py`. When creating/updating freelancers:
1. Receive `skillIds` array in request
2. Query Skill objects by ID
3. Use `.skills.append()` for relationship management
4. Use `.skills.clear()` + re-append for updates

### Error Handling Pattern

```python
from app.utils import handle_error, handle_success

# Success: return handle_success(data, 'Message', 200)
# Error: return handle_error('Error message', 400, optional_errors_dict)
```

Routes catch exceptions and map to appropriate HTTP status:
- `ValueError` → 400 or 404 (context-dependent)
- `ValidationError` (Marshmallow) → 400
- Unhandled exceptions → 500

### Response Format

All responses use standardized JSON structure:
```json
{
  "success": true/false,
  "message": "User-facing message",
  "data": {} or null
}
```

## Configuration & Environment

### .env Variables

- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` - MySQL connection
- `API_HOST`, `API_PORT` - Server binding (defaults: 0.0.0.0, 8000)
- `FLASK_ENV` - development/production/testing
- `CORS_ORIGINS` - Comma-separated allowed origins
- `SECRET_KEY` - Flask secret (defaults to 'dev-secret-key')

### Database Configuration

- `SQLALCHEMY_ECHO = True` - SQL logging enabled (shows query performance)
- `SQLALCHEMY_TRACK_MODIFICATIONS = False` - Disables unnecessary tracking
- `JSON_AS_ASCII = False` - Korean character support
- Testing uses in-memory SQLite database

## Common Development Tasks

### Adding a New API Endpoint

1. Define schema in `app/schemas/freelancer_schema.py` if data validation needed
2. Add service method in `app/services/freelancer_service.py`
3. Register route in `app/routes/freelancer_routes.py` with error handling
4. Test via curl or API client

### Modifying the Freelancer Model

1. Update `app/models/freelancer.py`
2. Database auto-creates on app startup via `db.create_all()`
3. For production migrations, use Flask-Migrate (pre-installed)

### Adding New Filters

1. Add filter logic in `FreelancerService.get_list()` query builder
2. Update `FreelancerCreateSchema`/`FreelancerUpdateSchema` if new input fields needed
3. Document in README.md API section

### Handling Many-to-Many Relationships

Use association table pattern (already implemented for Freelancer↔Skill):
```python
freelancer.skills.append(skill)  # Add
freelancer.skills.clear()         # Clear all
for skill in freelancer.skills:   # Iterate
```

## Important Notes

- All timestamps use UTC via `datetime.utcnow()`
- Freelancer IDs are UUID v4 strings
- Skill IDs are semantic strings (e.g., "react", "nodejs")
- Many-to-many queries use `.distinct()` to avoid duplicate results
- Schema `partial=True` used for update operations (optional fields)
- Phone validation expects format: "010-1234-5678"
