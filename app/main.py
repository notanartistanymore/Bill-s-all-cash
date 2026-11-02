from fastapi import FastAPI

from app.api.operations import router as router_operations
from app.api.wallets import router as router_wallets


app = FastAPI(title="Total all cash")
app.include_router(router=router_operations, tags=["Operations"])
app.include_router(router=router_wallets, tags=["Wallets"])