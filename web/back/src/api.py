import uvicorn
from fastapi import FastAPI

import routers.auth
import routers.groups
import routers.organization  # ToDo: Переделать на include_router()
from routers.index import router


def init_app() -> FastAPI:
    app = FastAPI(debug=True)
    app.include_router(router)
    return app


if __name__ == "__main__":
    uvicorn.run(init_app, port=8000)
