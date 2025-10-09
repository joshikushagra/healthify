# Healthify Backend API

A comprehensive, production-ready backend for the Healthify medical AI platform built with FastAPI, PostgreSQL, Redis, and OpenAI integration.

## 🚀 Features

- **Authentication & Authorization**: JWT-based auth with role-based access control
- **AI-Powered Chatbot**: OpenAI integration for symptom analysis and medical insights
- **Patient Management**: Complete patient profiles with medical history, allergies, and medications
- **Content Management**: Dynamic services and FAQ management
- **Caching & Performance**: Redis caching and rate limiting
- **Monitoring**: Prometheus metrics and Grafana dashboards
- **Background Tasks**: Celery for async processing
- **Security**: Comprehensive audit logging and data encryption
- **Testing**: Complete test suite with pytest
- **Documentation**: Auto-generated Swagger/OpenAPI docs

## 🛠 Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic
- **Cache**: Redis
- **AI**: OpenAI API + HuggingFace (optional)
- **Background Tasks**: Celery
- **Monitoring**: Prometheus + Grafana
- **Containerization**: Docker + Docker Compose
- **Testing**: Pytest

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
cd backend
cp env.example .env
# Edit .env with your configuration
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

```bash
# Create database
createdb healthify

# Run migrations
alembic upgrade head
```

### 4. Start Services

```bash
# Using Docker Compose (recommended)
docker-compose up -d

# Or run locally
uvicorn app.main:app --reload
```

### 5. Access the API

- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Grafana Dashboard**: http://localhost:3000 (admin/admin)

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/refresh` - Refresh access token
- `GET /auth/me` - Get current user profile
- `POST /auth/logout` - Logout user

### Chat & AI
- `POST /chat/symptom` - Analyze symptoms with AI
- `POST /chat/session` - Create chat session
- `GET /chat/sessions` - Get user's chat sessions
- `POST /chat/sessions/{id}/messages` - Send message
- `DELETE /chat/sessions/{id}` - End chat session

### Patient Management
- `GET /patients/me` - Get my patient profile
- `POST /patients/` - Create/update patient profile
- `GET /patients/me/medical-history` - Get medical history
- `POST /patients/me/medical-history` - Add medical history
- `GET /patients/me/allergies` - Get allergies
- `POST /patients/me/allergies` - Add allergy
- `GET /patients/me/medications` - Get medications
- `POST /patients/me/medications` - Add medication

### Content Management
- `GET /content/services` - Get all services
- `POST /content/services` - Create service (admin)
- `PUT /content/services/{id}` - Update service (admin)
- `DELETE /content/services/{id}` - Delete service (admin)
- `GET /content/faq` - Get FAQs
- `POST /content/faq` - Create FAQ (admin)
- `PUT /content/faq/{id}` - Update FAQ (admin)
- `DELETE /content/faq/{id}` - Delete FAQ (admin)

## 🔧 Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/healthify
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/healthify_test

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-super-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_ENABLED=True
```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## 📊 Monitoring

### Prometheus Metrics
- Available at `/metrics` endpoint
- Tracks API performance, database queries, and system health

### Grafana Dashboards
- Access at http://localhost:3000
- Default credentials: admin/admin
- Pre-configured dashboards for API metrics and system monitoring

## 🔒 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Patient, Doctor, Admin roles
- **Rate Limiting**: Redis-based rate limiting
- **Audit Logging**: Comprehensive audit trail
- **Data Encryption**: Sensitive data encryption
- **CORS Protection**: Configurable CORS settings
- **Input Validation**: Pydantic schema validation

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Scale services
docker-compose up -d --scale celery-worker=3
```

### Production Considerations

1. **Environment Variables**: Set all required environment variables
2. **Database**: Use managed PostgreSQL service
3. **Redis**: Use managed Redis service
4. **SSL/TLS**: Configure HTTPS
5. **Monitoring**: Set up proper monitoring and alerting
6. **Backup**: Regular database backups
7. **Security**: Regular security updates and audits

## 📝 API Documentation

The API documentation is automatically generated and available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the test cases for usage examples

## 🔄 Changelog

### v1.0.0
- Initial release
- Complete authentication system
- AI-powered symptom analysis
- Patient management
- Content management
- Monitoring and logging
- Comprehensive test suite
