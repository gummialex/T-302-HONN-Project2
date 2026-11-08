# T-302-HONN — Project 2

An event-driven ordering system built with **Python, FastAPI, PostgreSQL, RabbitMQ, and Docker Compose**.

The system manages buyers, merchants, products, and orders through a REST API layer. When an order is created, stock is reserved and payment is simulated by validating the card details. Successful payments reduce stock; failed payments release the reservation. Resend sends order and payment notifications to the buyer and merchant.

## Group members

Ernir, Guðmundur og Hafþór

## Startup

Docker Desktop must be running. Run the commands from the folder containing `docker-compose.yaml`.

1. Create `EmailService/.env` with your Resend credentials:

   ```dotenv
   RESEND_API_KEY=your_actual_api_key
   RESEND_FROM_EMAIL=your_verified_sender_email
   ```

   Do not commit or submit this file.

2. Build and start the system with two email workers:

   ```bash
   docker compose up -d --build --scale email-service=2
   ```

3. Check that the services have started:

   ```bash
   docker compose ps
   docker compose logs --tail=30 payment-service inventory-consumer email-service
   ```

4. Open **[http://localhost:8000/docs](http://localhost:8000/docs)** to use the API.

## API

Only the API layer is exposed locally, on port **8000**.

| Resource | Create | Retrieve |
| --- | --- | --- |
| Merchants | `POST /api/merchants` | `GET /api/merchants/{id}` |
| Buyers | `POST /api/buyers` | `GET /api/buyers/{id}` |
| Products | `POST /api/products` | `GET /api/products/{id}` |
| Orders | `POST /api/orders` | `GET /api/orders/{id}` |

Create a merchant and buyer first, then a product and an order using the returned IDs. Use valid recipient email addresses. Payment and email processing happen asynchronously after order creation; no money is charged.

## Logs and shutdown

```bash
docker compose logs -f
docker compose down
```

Named Docker volumes preserve database and RabbitMQ data between runs. Avoid `docker compose down -v` unless you intend to delete that data.
