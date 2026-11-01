# T-302-HONN – Project 2

An event-driven ordering system built with **Python (FastAPI), PostgreSQL, RabbitMQ, and Docker Compose**.

## Getting started

Install and start Docker Desktop, then run these commands from the project root:

```bash
# Start all services (once their Dockerfiles are ready)
docker compose up --build

# Or start just MerchantService and its PostgreSQL database
docker compose up --build merchant-service
```

## Service ports

| Service | Local address |
| --- | --- |
| OrderService | http://localhost:8000 |
| MerchantService | http://localhost:8001 |
| BuyerService | http://localhost:8002 |
| InventoryService | http://localhost:8003 |
| RabbitMQ management | http://localhost:15672 |

PaymentService and EmailService run internally without exposed HTTP ports. Each service with a database has its own PostgreSQL container and persistent Docker volume.

## Useful commands

```bash
docker compose ps                    # Running containers
docker compose logs -f merchant-service
docker compose down                  # Stop containers, keep database data
```

**Note:** The project is under development. Starting all services requires a working Dockerfile in each service folder. Avoid `docker compose down -v` unless you intend to delete the database volumes.
