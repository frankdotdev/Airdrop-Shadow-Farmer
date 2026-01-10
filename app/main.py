from fastapi import FastAPI
from app.api.v1.endpoints import wallet_routes, farming_routes, payment_routes, scanner_routes

app = FastAPI()

app.include_router(wallet_routes.router, prefix="/api/v1/wallets", tags=["wallets"])
app.include_router(farming_routes.router, prefix="/api/v1/farm", tags=["farm"])
app.include_router(payment_routes.router, prefix="/api/v1/payment", tags=["payment"])
app.include_router(scanner_routes.router, prefix="/api/v1/scan", tags=["scanner"])
