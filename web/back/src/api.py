import uvicorn
from fastapi import FastAPI

from routers import router


def init_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(router)
    return app


if __name__ == "__main__":
    uvicorn.run(init_app, port=8000)
