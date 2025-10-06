from contextlib import asynccontextmanager
import os
import uvicorn
from api.v1.routes import router as v1_router
from core.logger import logger
from infrastructure.event_bus.rabbitmq_publiser import RabbitMQPublisher
from middlewares.logging_middleware import LoggingMiddleware
from fastapi import FastAPI
from middlewares.exception_middleware import handler as exception_handler
from fastapi.middleware.cors import CORSMiddleware

app_logger = logger.getChild("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_logger.info("Starting application...")                
    yield
    app_logger.info("Shutting down application")

app = FastAPI(lifespan=lifespan, title="API write orders")

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],    
)
app.add_exception_handler(Exception, exception_handler)

app.include_router(v1_router, prefix="/v1", tags=["v1"])

@app.on_event("startup")
async def startup_event():
    global publisher_instance
    app_logger.debug("Connecting to RabbitMQ...")
    publisher_instance = RabbitMQPublisher(os.getenv("RABBITMQ_URL"))
    try:
        await publisher_instance.connect()
        app_logger.info("RabbitMQ connected successfully")
    except Exception as e:
        app_logger.error(f"Failed to connect to RabbitMQ: {str(e)}", exc_info=True)
        raise

@app.on_event("shutdown")
async def shutdown_event():
    global publisher_instance
    if publisher_instance:
        app_logger.debug("Closing RabbitMQ connection...")
        try:
            await publisher_instance.close()
            app_logger.info("RabbitMQ connection closed")
        except Exception as e:
            app_logger.error(f"Failed to close RabbitMQ connection: {str(e)}", exc_info=True)
            raise

if __name__ == "__main__":    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)