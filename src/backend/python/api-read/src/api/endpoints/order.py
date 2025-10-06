
import logging
import sys
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.dependencies import get_order_repository
from application.query.get_all_order import GetAllOrderQuery
from application.query.get_by_id_order import GetOrderQuery
from domain.repositories.mongo_order_repository_inteface import IMongoOrderRepository
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

logger.info("Inicio") 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.middleware("http")
async def log_exceptions(request: Request, call_next):
    try:
        logger.info("entrou middleware")
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Erro durante request {request.url.path}")  # log completo
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)},
        )   

@app.get("/")
async def root():
    return {"message": "API is working!"}  

@app.get("/orders/{order_id}")
async def get_order(order_id: str, repo: IMongoOrderRepository = Depends(get_order_repository)):
    query = GetOrderQuery(repo)
    try:
        order = await query.execute(order_id)
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@app.get("/orders")
async def get_all_order(repo: IMongoOrderRepository = Depends(get_order_repository)):
    query = GetAllOrderQuery(repo)
    try:
        order = await query.execute()
        return order
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))    