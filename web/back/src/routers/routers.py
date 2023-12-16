from pathlib import Path

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(Path(__file__).parent / "templates")


@router.get("/", name="index")
async def index(request: Request):
    """
    Index page just redirects to login page.
    """
    return RedirectResponse(url=request.url_for("login"))
