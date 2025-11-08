from fastapi import FastAPI

from core import config
from sources.api.v1.routers import incident

app = FastAPI(
    title="INCIDENT API-GATEWAY",
    docs_url="/docs/" if config.DEBUG else None,
    redoc_url="/redoc/" if config.DEBUG else None,
    version="v1",
    swagger_ui_parameters={"persistAuthorization": True}
)

for package in [incident]:
    app.include_router(package.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
