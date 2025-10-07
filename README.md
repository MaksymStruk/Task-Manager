# Task Manager API

A modern, async task management system built with FastAPI, Celery, and PostgreSQL. Features automatic task scheduling, status updates, and comprehensive API documentation.

## 🚀 Features

- **Async Task Management** - Create, update, delete, and track tasks
- **Automatic Scheduling** - Tasks are automatically marked as done when due date is reached
- **Real-time Status Updates** - Celery workers handle background processing
- **RESTful API** - Complete CRUD operations with comprehensive documentation
- **Docker Support** - Easy deployment with Docker Compose
- **Code Quality** - Perfect 10/10 Pylint score with comprehensive documentation

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - Async ORM for database operations
- **PostgreSQL** - Primary database
- **Celery** - Distributed task queue for background processing
- **Redis** - Message broker and result backend for Celery
- **Pydantic** - Data validation and serialization
- **Loguru** - Advanced logging

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📋 Prerequisites

- Docker and Docker Compose
- Git

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/MaksymStruk/Task-Manager.git
cd Task-Manager
```

### 2. Start the Application
```bash
docker compose up --build --detach
```

### 3. Access the Application
- **API Documentation**: http://localhost:8000/docs
- **API Root**: http://localhost:8000

## 📚 API Documentation

### Base URL
```
http://localhost:8000/
```

### Task Endpoints

#### Get All Tasks
```http
GET /api/v1/task/
```
**Query Parameters:**
- `skip` (int, optional): Number of tasks to skip (default: 0)
- `limit` (int, optional): Maximum tasks to return (default: 100)

#### Get Task by ID
```http
GET /api/v1/task/{task_id}
```

#### Create Task
```http
POST /api/v1/task/
```
**Request Body:**
```json
{
    "title": "Task title (required, 1-255 chars)",
    "description": "Brief description (optional)",
    "text": "Detailed content (optional)",
    "due_date": "2025-12-31T23:59:59Z",
    "status": "PENDING"
}
```

#### Update Task
```http
PUT /api/v1/task/{task_id}
```
**Request Body:** (all fields optional)
```json
{
    "title": "Updated title",
    "due_date": "2025-12-25T12:00:00Z",
    "status": "DONE"
}
```

#### Delete Task
```http
DELETE /api/v1/task/{task_id}
```

#### Get Tasks by Status
```http
GET /api/v1/task/status/{status}
```
**Status Values:** `pending`, `done`

### Health Endpoints

#### API Root
```http
GET /
```

#### Health Check
```http
GET /health
```

## 🏗️ Project Structure

```
Task_Manager/
├── backend/
│   ├── app/
│   │   ├── core/           # Configuration and middleware
│   │   ├── db/             # Database configuration
│   │   ├── log/            # Logging setup
│   │   ├── models/         # SQLAlchemy models
│   │   ├── routers/        # API endpoints
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── workers/        # Celery tasks
│   └── requirements.txt    # Python dependencies
└── docker-compose.yml      # Container orchestration
```

## 🔧 Development

### Code Quality Check
```bash
pylint backend/app/ --rcfile=backend/.pylintrc
```

### View Logs
```bash
docker compose logs -f backend
docker compose logs -f celery
docker compose logs -f celery-beat
```

## 📊 Task Lifecycle

1. **Creation** - Task created with due date
2. **Scheduling** - Celery automatically schedules status update
3. **Processing** - Background worker checks due date
4. **Completion** - Task marked as DONE when due date is reached

## 🔍 Key Features

### Automatic Task Management
- Tasks are automatically marked as DONE when their due date is reached
- Background Celery workers handle status updates
- Redis provides reliable message queuing

### Async Architecture
- Fully async FastAPI application
- Async SQLAlchemy for database operations
- Celery workers use asyncio.run() for async database access

### Code Quality
- Perfect 10/10 Pylint score
- Comprehensive docstrings throughout
- Type hints and validation
- Professional API documentation

## 🐳 Docker Services

- **backend** - FastAPI application (port 8000)
- **postgres** - PostgreSQL database (port 5432)
- **redis** - Redis server (port 6379)
- **celery** - Celery worker for background tasks

## 📝 Environment Variables

Key environment variables (with defaults):
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `CELERY_BROKER_URL` - Celery message broker
- `DEBUG` - Enable debug mode (default: True)

## 🚨 Important Notes

- **Database**: PostgreSQL is used as the primary database
- **Background Tasks**: Celery workers handle automatic task status updates
- **Async Operations**: All database operations are fully asynchronous
- **API Documentation**: Available at `/docs` endpoint
- **Logging**: Comprehensive logging with Loguru

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**: Ensure ports 8000, 5432, 6379 are available
2. **Database Connection**: Wait for PostgreSQL to fully start before accessing API
3. **Celery Workers**: Check logs if background tasks aren't processing

### Useful Commands
```bash
# Restart all services
docker compose restart

# Rebuild and restart
docker compose up --build --detach

# View all logs
docker compose logs -f

# Stop all services
docker compose down
```

## 📈 Performance

- **Async Operations** - Non-blocking database operations
- **Connection Pooling** - Efficient database connection management
- **Background Processing** - Celery handles heavy operations
- **Caching** - Redis provides fast data access

## 🎯 Production Deployment

For production deployment:
1. Set `DEBUG=False` in environment variables
2. Use production PostgreSQL and Redis instances
3. Configure proper logging levels
4. Set up monitoring for Celery workers
5. Use reverse proxy (nginx) for load balancing

---

**Built with ❤️ using FastAPI, Celery, and modern async Python**
