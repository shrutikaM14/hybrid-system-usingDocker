# Hybrid System Using Docker

## Project Overview

This project is a hybrid multi-database system built using Docker and FastAPI.

The system integrates:

- PostgreSQL (Relational SQL Database)
- MongoDB (NoSQL Document Database)
- Neo4j (Graph Database)

All services run inside Docker containers using Docker Compose.

---

# Technologies Used

- Docker
- Docker Compose
- FastAPI
- PostgreSQL
- MongoDB
- Neo4j
- Swagger UI
- Python

---

# System Architecture

FastAPI acts as the API layer and communicates with multiple databases.

FastAPI
├── PostgreSQL
├── MongoDB
└── Neo4j

---

# Features

## PostgreSQL
- Store relational user data
- SQL queries
- CRUD operations

## MongoDB
- Store product documents
- NoSQL document operations

## Neo4j
- Store graph relationships
- Friendship connections
- Graph queries using Cypher

---

# Docker Containers

- fastapi-container
- postgres-container
- mongodb-container
- neo4j-container

---

# Ports Used

| Service | Port |
|---|---|
| FastAPI | 8000 |
| PostgreSQL | 5433 |
| MongoDB | 27018 |
| Neo4j Browser | 7474 |
| Neo4j Bolt | 7687 |

---

# Run Project

## Start Containers

```bash
sudo docker compose up -d
