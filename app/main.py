from fastapi import FastAPI
from app.api.v1.routes import products, users, auth, movements

app = FastAPI()

app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(movements.router, prefix="/api/v1/movements", tags=["Movements"])