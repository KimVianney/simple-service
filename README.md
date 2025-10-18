# Profile API - FastAPI Implementation

A FastAPI-based REST API that provides user profile information integrated with the Cat Facts API.

## Features

- ✅ GET `/me` endpoint returning user profile with cat facts
- ✅ Dynamic timestamp generation in ISO 8601 format
- ✅ Cat Facts API integration with error handling
- ✅ Environment variables for configuration
- ✅ CORS support
- ✅ Comprehensive logging
- ✅ Graceful error handling with fallback messages
- ✅ Proper timeout handling for external API calls

## Requirements

- Python 3.8+
- pip

## Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd /Users/vianneyk/Code/hng/backend/stage-zero
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your information:
   ```
   USER_EMAIL=your.email@example.com
   USER_NAME=Your Full Name
   USER_STACK=Python/FastAPI
   ```

## Running the API

**Development mode:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/me`
Returns user profile information with a random cat fact.

**Response (200 OK):**
```json
{
  "status": "success",
  "user": {
    "email": "your.email@example.com",
    "name": "Your Full Name",
    "stack": "Python/FastAPI"
  },
  "timestamp": "2025-10-18T12:34:56.789Z",
  "fact": "Cats have over 20 vocalizations."
}
```

**Headers:**
- Content-Type: `application/json`

### GET `/`
Root endpoint with API information.

### GET `/health`
Health check endpoint.

## Testing

**Using curl:**
```bash
curl http://localhost:8000/me
```

**Using httpie:**
```bash
http GET http://localhost:8000/me
```

**Using browser:**
Navigate to `http://localhost:8000/me`

## Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Error Handling

The API gracefully handles Cat Facts API failures by:
- Using a timeout of 5 seconds for external API calls
- Catching network errors and timeouts
- Returning a fallback message if the external API is unavailable
- Logging all errors for debugging

## Best Practices Implemented

- ✅ Environment variables for configuration
- ✅ CORS headers for cross-origin requests
- ✅ Structured logging for debugging
- ✅ Proper error handling and HTTP status codes
- ✅ Type hints with Pydantic models
- ✅ Async/await for non-blocking operations
- ✅ Timeout configuration for external API calls
- ✅ ISO 8601 timestamp format
- ✅ Dynamic data on every request (no caching)

## Project Structure

```
stage-zero/
├── main.py              # Main FastAPI application
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore file
├── README.md           # This file
└── INSTRUCT.md         # Task instructions
```

## Technology Stack

- **Framework:** FastAPI 0.119.0
- **ASGI Server:** Uvicorn 0.38.0
- **HTTP Client:** httpx 0.27.0
- **Data Validation:** Pydantic 2.12.3
- **Environment:** python-dotenv 1.0.0

## Deployment Notes

For production deployment:

1. Set appropriate CORS origins in `main.py`
2. Configure environment variables securely
3. Consider implementing rate limiting
4. Use a production ASGI server with multiple workers
5. Set up monitoring and logging aggregation
6. Use HTTPS with proper SSL certificates

Example production command:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## License

This project is part of the HNG Backend Stage Zero task.

