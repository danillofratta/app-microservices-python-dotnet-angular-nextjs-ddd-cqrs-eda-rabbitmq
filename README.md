\##  🛒 E-commerce System

A multi-platform E-commerce System demonstrating DDD, CQRS, and EDA with Python (FastAPI), .NET (ASP.NET Core), Angular, and Next.js.
The system uses RabbitMQ for event-driven communication, PostgreSQL for write operations, and MongoDB for read operations.

\## ⚙️ Process Overview

\- The Angular frontend creates an order and calls the Python write API.
\- The Python API saves the order data in PostgreSQL.
\- The Python API publishes an OrderCreatedEvent message to RabbitMQ.
\- The Python consumer reads the event and saves the data in MongoDB (read model).
\- The .NET consumer listens to the same event, checks product stock, and sends a StockReservedEvent (OK or not OK) back to RabbitMQ.
\- The Python consumer listens for the StockReservedEvent, updates the order status in PostgreSQL and MongoDB.
\- The Angular frontend calls the Python read API to display orders from MongoDB.
\- The Next.js frontend calls the .NET API to manage and save product data in PostgreSQL.

\## Technologies

\- Backend: Python (FastAPI), .NET (ASP.NET Core)

\- Frontend: Angular 17, Next.js 14

\- Messaging: RabbitMQ

\- Databases: PostgreSQL, MongoDB

\- Containerization: Docker



\## Setup

1\. Install dependencies:

&nbsp;  - Python: `pip install -r src/backend/python/requirements.txt`

&nbsp;  - .NET: `dotnet restore src/backend/dotnet/EcommerceSystem.sln`

&nbsp;  - Angular: `npm install` in `src/frontend/angular`

&nbsp;  - Next.js: `npm install` in `src/frontend/nextjs`

2\. Start services: `docker-compose up -d`

3\. Run APIs:

&nbsp;  - Python: `python src/backend/python/main.py`

&nbsp;  - .NET: `dotnet run --project src/backend/dotnet/Api`

4\. Run frontends:

&nbsp;  - Angular: `ng serve` in `src/frontend/angular`

&nbsp;  - Next.js: `npm run dev` in `src/frontend/nextjs`

5\. Access:

&nbsp;  - Python API: `http://localhost:8000/docs`

&nbsp;  - .NET API: `http://localhost:8080/swagger`

&nbsp;  - Angular: `http://localhost:4200`

&nbsp;  - Next.js: `http://localhost:3000`

&nbsp;  - RabbitMQ: `http://localhost:15672` (user: guest, pass: guest)



\## Architecture

\- \*\*DDD\*\*: Domain entities (Order, Product), aggregates, and events.

\- \*\*CQRS\*\*: Separate write (Postgres) and read (MongoDB) models.

\- \*\*EDA\*\*: RabbitMQ for async communication (`OrderCreatedEvent`, `StockReservedEvent`).

TODO
- create containers
- create save products api .net

Scripts DB postgresql:

CREATE TABLE IF NOT EXISTS public."Products"
(
    "Name" text COLLATE pg_catalog."default",
    "Price" numeric,
    "Stock" bigint,
    "Id" uuid
)

CREATE TABLE IF NOT EXISTS public."Orders"
(
    id text COLLATE pg_catalog."default" NOT NULL,
    customer_id text COLLATE pg_catalog."default",
    items text COLLATE pg_catalog."default",
    status text COLLATE pg_catalog."default",
    created_at timestamp without time zone,
    total numeric,
    CONSTRAINT orders_pkey PRIMARY KEY (id)
)
