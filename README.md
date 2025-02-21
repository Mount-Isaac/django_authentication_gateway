# Django Authentication GATEWAY

A centralized authentication gateway for microservices architecture that handles authentication and request forwarding to multiple backend services.

## Overview

This Django-based authentication bridge serves as a central gateway for all microservices in your architecture. It provides:
- Single point of authentication
- Request forwarding to microservices
- Unified error handling
- Centralized monitoring

## Features

- JWT-based authentication
- Request proxying to multiple microservices
- Automatic token validation
- Request/Response transformation
- Error handling and logging
- Service health monitoring

## Prerequisites

- Python 3.8+
- Django 4.0+
- PostgreSQL/MySQL (for token storage)

## Installation

1. Clone the repository:
```bash
git clone git@github.com:Mount-Isaac/django_authentication_gateway.git
cd django-authentication-gateway
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
```

## Configuration

### 1. Environment Variables

```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
JWT_SECRET_KEY=your-jwt-secret
```

### 2. Microservices Configuration

Add your microservices in `config.yaml`:

```python
MICROSERVICES = {
    'service1': {
        'url': 'http://service1:5000',
        'timeout': 30,
    },
    'service2': {
        'url': 'http://service2:5001',
        'timeout': 30,
    }
}
```

## Usage

### 1. Authentication Flow

1. Client requests authentication token:
   - POST `/api/auth/token/`
   - Receives JWT token

2. Use token for subsequent requests:
   - Add header: `Authorization: Bearer <token>`
   - Gateway validates token
   - Forwards request to appropriate service

### 2. Request Forwarding

- Original request: `GET /service1/users/`
- Gateway authenticates request
- Forwards to: `http://service1:5000/users/`
- Returns response to client

## Security Considerations

1. Always use HTTPS in production
2. Configure appropriate token expiration times
3. Implement rate limiting
4. Sanitize headers and request data
5. Monitor for suspicious activities

## Monitoring

The gateway provides monitoring endpoints:

- `/health/` - System health status
- `/metrics/` - Performance metrics
- `/services/status/` - Microservices status

## Development

### Setting Up Development Environment

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Run tests:
```bash
python manage.py test
```

### Adding New Services

1. Add service configuration to `MICROSERVICES` in settings
2. Configure routing rules if needed
3. Test connectivity and authentication

## Troubleshooting

Common issues and solutions:

1. Token validation failures:
   - Check token expiration
   - Verify JWT secret key
   - Ensure correct token format

2. Service connection issues:
   - Verify service URLs
   - Check network connectivity
   - Confirm service health

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request
4. Follow coding standards
5. Include tests for new features

## Contact

For support or queries:
- Email: isadechair019@gmail.com
- ASAP response : [Whatsapp](https://api.whatsapp.com/send/?phone=254759856000&text&type=phone_number&app_absent=0)


### <i style="background-color: green">DJANGO UNIX HINT: start many apps at a go using this command: </i>
```bash 
for app in app_1 app_2 app_3; do python manage.py startapp $app; done
```