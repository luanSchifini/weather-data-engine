# Weather Data Engine 🌦️

A production-ready weather data pipeline and REST API that integrates with the OpenWeather API to collect, store, and analyze weather data. Built with FastAPI, PostgreSQL, and Docker.

## Overview

This project provides a complete weather data solution with:
- **Data Collection**: Fetch real-time weather data from OpenWeather API
- **Storage**: Persist weather records in PostgreSQL
- **REST API**: Query historical data and city statistics
- **Analytics**: Calculate temperature min/max/average per city
- **Containerized**: Fully dockerized with Docker Compose

### Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Docker** - Containerization
- **Uvicorn** - ASGI server

## Prerequisites

- Docker & Docker Compose
- OpenWeather API Key ([Get one free here](https://openweathermap.org/api))

## Quick Start

### 1. Clone and Configure

```bash
git clone <repository-url>
cd weather-data-engine
cp .env.example .env
```

### 2. Add Your API Key

Edit `.env` and add your OpenWeather API key:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

### 3. Start the Application

```bash
docker-compose up --build
```

The API will be available at **http://localhost:8000**

### 4. Test It Out

Check health:
```bash
curl http://localhost:8000/health
```

Collect weather data:
```bash
curl -X POST http://localhost:8000/api/v1/weather/collect/London
```

Get city statistics:
```bash
curl http://localhost:8000/api/v1/weather/stats/London
```

## API Documentation

Once running, access the interactive API docs:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Development

### Run Tests

```bash
docker-compose exec api pytest
```

## Project Structure

```
weather-data-engine/
├── app/
│   ├── api/endpoints/     # API route handlers
│   ├── models/            # SQLAlchemy models
│   ├── repositories/      # Data access layer
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── main.py            # FastAPI application
├── tests/                 # Test suite
├── docker-compose.yaml    # Docker orchestration
├── Dockerfile             # Container definition
└── requirements.txt       # Python dependencies
```

## License

Created as part of the GnTech technical challenge.