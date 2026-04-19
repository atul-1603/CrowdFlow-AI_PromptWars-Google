# CrowdFlow AI Architecture

This document describes the Domain-Driven Design (DDD) of CrowdFlow AI.

## Backend
- **api/**: FastAPI routes for HTTP transport.
- **domain/**: Core business logic separated by domains:
  - `crowd/`: Sensor data processing.
  - `routing/`: Navigating the stadium.
  - `queue/`: Latency predictions.
  - `recommendation/`: User suggestions.
- **agents/**: The AI orchestration layer using Antigravity and Vertex AI.
- **integrations/**: External providers (Firebase, Maps, Vertex AI).

## Frontend
Next.js React app using App Router. Structured by features (`chat`, `map`, `dashboard`) instead of by components.
