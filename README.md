# Electrical Load Calculation API

Backend API built with FastAPI to manage electrical projects and perform power load calculations.

## Overview

This project simulates a real-world engineering workflow where users can define an electrical distribution architecture and compute load balances.

The focus is on backend design, scalability, and clean architecture rather than UI.

---

## Features

- User authentication (JWT)
- Project management
- Hierarchical electrical structure (e.g. main board, sub-distribution)
- Consumer definition (power, quantity, simultaneity factor)
- Load calculation
- Calculation history

---

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Pytest

---

## Getting Started

### Run with Docker

```
docker compose up --build
```

API will be available at:

```
http://localhost:8000
```

Docs:

```
http://localhost:8000/docs
```

---

## Project Structure

- `app/routes` → API endpoints
- `app/services` → business logic
- `app/models` → database models
- `app/schemas` → data validation

---

## Documentation

Detailed project specification available in:

```
PROJECT_SPEC.md
```

---

## Goals

This project is designed to:

- demonstrate backend engineering skills
- handle real-world business logic
- be production-ready (Docker, tests, scalable design)

---

## Status

Work in progress. Features are being implemented iteratively.