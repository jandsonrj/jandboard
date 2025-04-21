from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.database import engine
from app import models
from app.auth import router as auth_router
from app.routers import user, task

models.Base.metadata.create_all(bind=engine)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)





@app.get("/")
def read_root():
    return {"message": "JandBoard Backend API 🚀 tá no ar!"}

# ROTAS
app.include_router(auth_router, prefix="/auth")
app.include_router(user.router)
app.include_router(task.router)

# 🔐 Swagger customizado para aceitar Bearer token manualmente
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="JandBoard Backend API",
        version="1.0.0",
        description="API do Projeto JandBoard com autenticação JWT manual 🎯",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
