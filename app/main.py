from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.routes import products


app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(
    products.router,
    prefix=f"{settings.API_V1_STR}/products",
    tags=["Products"],
)


@app.get("/")
def root():
    return {"message": "Inventory Management API is running"}
