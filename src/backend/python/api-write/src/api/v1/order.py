# import logging
# import sys
# from fastapi import Body, Depends, FastAPI, HTTPException, Request
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel
# from application.commands.create_order import CreateOrderCommand
# from application.dependencies import get_create_order_command
# from application.dtos.create_order_dto import CreateOrderDto
# from domain.entities.order import Order
# from infrastructure.event_bus.rabbitmq_publiser import RabbitMQPublisher
# from fastapi.middleware.cors import CORSMiddleware
# import os
# from dotenv import load_dotenv

# logging.basicConfig(
#     level=logging.INFO, 
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     handlers=[logging.StreamHandler(sys.stdout)]
# )

# logger = logging.getLogger(__name__)

# logger.info("Inicio") 
# load_dotenv()

# app = FastAPI()

# class OrderOut(BaseModel):
#     order_id:str

# @app.on_event("startup")
# async def startup_event():
#     global publisher_instance
#     publisher_instance = RabbitMQPublisher(os.getenv("RABBITMQ_URL"))    
#     await publisher_instance.connect()

# @app.on_event("shutdown")
# async def shutdown_event():
#     if publisher_instance:
#         await publisher_instance.close()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

# @app.middleware("http")
# async def log_exceptions(request: Request, call_next):
#     try:
#         logger.info("entrou middleware")
#         return await call_next(request)
#     except Exception as e:
#         logger.exception(f"Erro durante request {request.url.path}")  
#         return JSONResponse(
#             status_code=500,
#             content={"detail": str(e)},
#         )

# @app.get("/")
# async def root():
#     return {"message": "API is working!"}

# @app.post("/orders/",response_model=OrderOut)
# async def create_order(
#     dto: CreateOrderDto,
#     command: CreateOrderCommand = Depends(get_create_order_command)    
# ):
#     logger.info("Start create_order")
#     try:
#         orderOut = OrderOut(await command.execute(dto.customer_id, dto.items))
#         logger.info("create_order OK")
#         return {"order_id": orderOut}
#     except Exception as e:
#         logger.exception("Erro ao criar order")
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:        
#         logger.info("Publisher fechado")
