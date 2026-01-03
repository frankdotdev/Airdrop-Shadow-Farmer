from fastapi import FastAPI
from app.api.v1.endpoints import wallet_routes, farming_routes

app = FastAPI()

app.include_router(wallet_routes.router, prefix="/wallets", tags=["wallets"])
app.include_router(farming_routes.router, prefix="/farm", tags=["farm"])