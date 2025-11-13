# Django Authentication Gateway

![Project Flow Chart](./images/project_design.png)


## Features

- JWT-based authentication (OAuth2 ready)
- Token validation middleware
- Proxying/forwarding to internal services
- Request/response transformation
- Role/permission middleware
- Basic service health-check endpoints

## Docker

Pull from Docker Hub:

```bash
docker pull theisaac/django_authentication_gateway:latest
```

## Requirements

- Python 3.9+
- Django 4.2+
- PostgreSQL / MySQL 


## Setup

```bash
# 1. Clone repo
git clone https://github.com/Mount-Isaac/django_authentication_gateway.git
cd django_authentication_gateway

# 2. Virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate for Windows

# 3. Install deps
pip install -r requirements.txt

# 4. Configure .env: rename the .env.example file & populate with the correct credentials
cp .env.example .env

# 4. Run the application
python manage.py runserver 1819
```

## Environment Variables

```env
DEBUG=False
SECRET_KEY=your-django-secret
DATABASE_URL=postgres://user:password@localhost/db
JWT_SECRET_KEY=your-jwt-secret
```

## Microservice Routing

Define services in `config.yaml` or directly in `settings.py`:

```yaml
microservices:
  orders:
    url: http://localhost:5000
    timeout: 30
    authorization: true
    forward:
      headers: true
      body: true
      params: true

  users:
    url: http://localhost:5001
    timeout: 30
    authorization: false
    forward:
      headers: true
      body: false
      params: true

  inventory:
    url: http://localhost:5002
    timeout: 45
    authorization: true
    forward:
      headers: true
      body: true
      params: true
```

## Authentication Flow

1. `POST /api/auth/token/` — get a JWT token
2. Add header: `Authorization: Bearer <token>`
3. Gateway validates token
4. Routes request to correct microservice



## Response structure

### Success
```bash
{
  "success": True,
  "message": "Action completed successfully",
  "data": {...},
  "meta": { "request_id": "...", "timestamp": "..." }
}
```


### Error
```bash
{
  "success": False,
  "message": "Order not found",
  "code": 404,
  "error": {
    "type": "NotFoundError",
    "details": "Order with ID 9876 not found"
  },
  "meta": { "request_id": "...", "timestamp": "..." }
}
```



## Monitoring Endpoints

| Endpoint | Description |
|----------|-------------|
| `/health/` | Gateway health check |
| `/metrics/` | Performance stats |
| `/services/status/` | Microservice availability |


## Dev & Testing

```bash
# Install dev tools
pip install -r requirements-dev.txt

# Run tests
python manage.py test
```


## Add a New Microservice

1. Register it in `microservices` config.yaml
2. Set up any auth or routing rules if needed
3. Deploy and test


## Security

- Use HTTPS in production
- Short-lived access tokens
- Rate limiting (via caching or middleware)
- Header sanitization
- IP + request logging


## Contact

- Email: **isadechair019@gmail.com**
- WhatsApp: [Chat Now](https://api.whatsapp.com/send/?phone=254759856000)

---

## Pro Tip

Start multiple Django apps at once:

```bash
for app in app1 app2 app3; do python manage.py startapp $app; done
```
