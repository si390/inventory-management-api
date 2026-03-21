from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes import products, users, auth, movements


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(
    products.router,
    prefix=f"{settings.API_V1_STR}/products",
    tags=["Products"],
)
app.include_router(
    users.router,
    prefix=f"{settings.API_V1_STR}/users",
    tags=["Users"],
)

app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["Auth"],
)

app.include_router(
    movements.router,
    prefix=f"{settings.API_V1_STR}/movements",
    tags=["Movements"],
)

@app.get("/")
def root():
    return {"message": "Inventory Management API is running"}
