from fastapi import APIRouter,  Depends, HTTPException
from application.commands.create_order import CreateOrderCommand
from application.dependencies import get_create_order_command
from application.dtos.create_order_dto import CreateOrderDto
from application.dtos.order_out import OrderOut
from core.logger import logger

router = APIRouter()

route_logger = logger.getChild("routes")

@router.get("/")
async def root():
    return {"message": "API is working!"}

@router.post("/orders/", response_model=OrderOut)
async def create_order(
    dto: CreateOrderDto,
    command: CreateOrderCommand = Depends(get_create_order_command)    
):    
    route_logger.info(f"Received POST /v1/orders/ request: customer_id={dto.customer_id}, items_count={len(dto.items)}")
    try:        
        result = await command.execute(dto.customer_id, dto.items)
        route_logger.info(f"Order created: order_id={result.order_id}, total={result.total}")
        return result
    except Exception as e:        
        route_logger.error(f"Failed to create order: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
